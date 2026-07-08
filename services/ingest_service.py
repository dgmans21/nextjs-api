import uuid
from typing import Any

from models.entities import StoreEvent
from models.interfaces.event_repository import EventRepository
from schemas.event import IngestRequestSchema, IngestResponseSchema
from services.db import DbService
from services.kafka_producer import KafkaProducerService
from services.model_inference import predict
from utils.exceptions import ConflictAppError
from utils.logger import api_logger, kafka_logger


class IngestService:
  def __init__(
    self,
    db_service: DbService,
    event_repository: EventRepository,
    kafka_producer: KafkaProducerService,
  ) -> None:
    self._db_service = db_service
    self._event_repository = event_repository
    self._kafka_producer = kafka_producer
    self._request_schema = IngestRequestSchema()
    self._response_schema = IngestResponseSchema()

  def ingest(self, payload: dict) -> dict:
    data = self._request_schema.load(payload)
    event_id = data.get("event_id") or self._generate_event_id()

    if self._event_repository.find_by_id(event_id) is not None:
      raise ConflictAppError(f"Event already exists: {event_id}")

    event = StoreEvent(
      event_id=event_id,
      event_type=data["event_type"],
      channel=data["channel"],
      message=data.get("message"),
      severity=data.get("severity"),
      severity_hint=data.get("severity_hint"),
      sentiment=data.get("sentiment"),
      status=data.get("status", "open"),
      requires_response=data.get("requires_response", True),
      confidence=data.get("confidence"),
      predicted_type=data.get("predicted_type"),
      timestamp=data.get("timestamp"),
    )

    event_payload = event.to_dict()
    published = self._kafka_producer.publish_event(event_payload)

    if published:
      kafka_logger.info("Ingest queued via Kafka: %s", event_id)
      queued_event = StoreEvent(
        event_id=event.event_id,
        event_type=event.event_type,
        channel=event.channel,
        status="queued",
        requires_response=event.requires_response,
        message=event.message,
        severity=event.severity,
        severity_hint=event.severity_hint,
        sentiment=event.sentiment,
        confidence=event.confidence,
        predicted_type=event.predicted_type,
        timestamp=event.timestamp,
      )
      message = "Event queued to Kafka"
      created = queued_event
    else:
      api_logger.info("Kafka unavailable, SQLite fallback: %s", event_id)
      created = self._db_service.insert_event(event)
      message = "Event ingested successfully (SQLite fallback)"

    response = {
      "message": message,
      "event": created.to_dict(),
      "analysis": self._build_inline_analysis(created),
    }
    return self._response_schema.dump(response)

  def _build_inline_analysis(self, event: StoreEvent) -> dict:
    """POST /ingest 응답용 인라인 분석. DB analyses 테이블에는 저장하지 않는다."""
    prediction = predict(event)
    return {
      "predicted_type": prediction.predicted_type,
      "sentiment": "neutral",
      "severity": prediction.severity,
      "confidence": prediction.confidence,
      "source": prediction.source,
    }

  def ingest_from_kafka_payload(self, payload: dict[str, Any]) -> StoreEvent:
    event = StoreEvent(
      event_id=payload["event_id"],
      event_type=payload["event_type"],
      channel=payload["channel"],
      status=payload.get("status", "open"),
      requires_response=bool(payload.get("requires_response", True)),
      message=payload.get("message"),
      severity=payload.get("severity"),
      severity_hint=payload.get("severity_hint"),
      sentiment=payload.get("sentiment"),
      confidence=payload.get("confidence"),
      predicted_type=payload.get("predicted_type"),
      timestamp=payload.get("timestamp"),
    )

    existing = self._event_repository.find_by_id(event.event_id)
    if existing is None:
      return self._db_service.insert_event(event)
    return existing

  def _generate_event_id(self) -> str:
    return f"evt-{uuid.uuid4().hex[:8]}"
