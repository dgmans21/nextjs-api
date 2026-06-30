from models.entities import AnalysisRecord, StoreEvent
from models.interfaces.analysis_repository import AnalysisRepository
from services.db import DbService
from services.model_inference import predict
from utils.exceptions import NotFoundAppError


class AnalysisService:
  def __init__(self, db_service: DbService, analysis_repository: AnalysisRepository) -> None:
    self._db_service = db_service
    self._analysis_repository = analysis_repository

  def get_analysis(self, event_id: str) -> dict:
    event = self._db_service.get_event(event_id)
    if event is None:
      raise NotFoundAppError(f"Event not found: {event_id}")

    analysis = self._analysis_repository.find_by_event_id(event_id)
    if analysis is None:
      analysis = self._run_inference(event)

    return {
      "event": event.to_dict(),
      "analysis": self._analysis_to_response(analysis),
    }

  def _run_inference(self, event: StoreEvent) -> AnalysisRecord:
    prediction = predict(event)
    analysis = AnalysisRecord(
      event_id=event.event_id,
      predicted_type=prediction.predicted_type,
      sentiment="neutral",
      severity=prediction.severity,
      confidence=prediction.confidence,
      source=f"rule-based:{prediction.summary}",
    )
    self._db_service.update_analysis(analysis)

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
    self._db_service.update_event(updated_event)
    return analysis

  def _analysis_to_response(self, analysis: AnalysisRecord) -> dict:
    payload = analysis.to_dict()
    if payload.get("source", "").startswith("rule-based:"):
      payload["source"] = "rule-based"
    return payload
