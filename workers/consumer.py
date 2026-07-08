"""
Kafka consumer worker (Flask-independent, no HTTP server).

Run:
  python -m workers.consumer
"""

import json
import logging
import os

os.environ.setdefault("PYTHONUTF8", "1")

from config import Config
from database.factory import create_database_adapter
from models.entities import AnalysisRecord, StoreEvent
from models.repositories.analysis_repository import AnalysisRepositoryImpl
from models.repositories.event_repository import EventRepositoryImpl
from services.db import DbService
from services.model_inference import init_inference, predict
from utils.logger import kafka_logger


def process_event(db_service: DbService, analysis_repository: AnalysisRepositoryImpl, payload: dict) -> None:
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

  existing = db_service.get_event(event.event_id)
  if existing is None:
    db_service.insert_event(event)
    kafka_logger.info("Worker saved event: %s", event.event_id)
  else:
    event = existing

  prediction = predict(event)
  analysis = AnalysisRecord(
    event_id=event.event_id,
    predicted_type=prediction.predicted_type,
    sentiment="neutral",
    severity=prediction.severity,
    confidence=prediction.confidence,
    source=f"{prediction.source}:{prediction.summary}",
  )
  db_service.update_analysis(analysis)

  updated_event = StoreEvent(
    event_id=event.event_id,
    event_type=event.event_type,
    channel=event.channel,
    status="analyzed",
    requires_response=prediction.action_required,
    message=event.message,
    severity=prediction.severity,
    severity_hint=event.severity_hint,
    sentiment=analysis.sentiment,
    confidence=prediction.confidence,
    predicted_type=prediction.predicted_type,
    timestamp=event.timestamp,
  )
  db_service.update_event(updated_event)
  kafka_logger.info("Worker analyzed event: %s", event.event_id)


def run_consumer(config: Config) -> None:
  if not config.KAFKA_ENABLED:
    kafka_logger.error("KAFKA_ENABLED=0 — consumer cannot start")
    return

  init_inference(config)

  try:
    from kafka import KafkaConsumer
  except ImportError:
    kafka_logger.error("kafka-python is not installed")
    return

  adapter = create_database_adapter(config)
  adapter.connect()
  adapter.initialize_schema()

  event_repository = EventRepositoryImpl(adapter)
  analysis_repository = AnalysisRepositoryImpl(adapter)
  db_service = DbService(adapter, event_repository, analysis_repository)

  consumer = KafkaConsumer(
    config.KAFKA_TOPIC,
    bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS.split(","),
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    group_id="ops-worker",
    auto_offset_reset="earliest",
  )

  kafka_logger.info("Worker consumer started on topic: %s", config.KAFKA_TOPIC)

  for message in consumer:
    try:
      process_event(db_service, analysis_repository, message.value)
    except Exception as error:
      kafka_logger.exception("Worker failed to process message: %s", error)


if __name__ == "__main__":
  logging.basicConfig(level=Config.LOG_LEVEL)
  run_consumer(Config())
