from models.entities import AnalysisRecord, StoreEvent
from models.interfaces.analysis_repository import AnalysisRepository
from models.interfaces.event_repository import EventRepository


class EventRepositoryImpl(EventRepository):
  def __init__(self, adapter) -> None:
    from database.base import DatabaseAdapter

    self._adapter: DatabaseAdapter = adapter

  def find_all(self) -> list[StoreEvent]:
    return [self._row_to_event(row) for row in self._adapter.fetch_all_events()]

  def find_by_id(self, event_id: str) -> StoreEvent | None:
    row = self._adapter.fetch_event_by_id(event_id)
    return self._row_to_event(row) if row else None

  def count(self) -> int:
    return self._adapter.count_events()

  def create(self, event: StoreEvent) -> StoreEvent:
    self._adapter.insert_event(self._event_to_dict(event))
    return event

  def update(self, event: StoreEvent) -> StoreEvent:
    self._adapter.update_event(self._event_to_dict(event))
    return event

  def delete(self, event_id: str) -> bool:
    existing = self.find_by_id(event_id)
    if existing is None:
      return False
    self._adapter.delete_event(event_id)
    return True

  def _row_to_event(self, row: dict) -> StoreEvent:
    return StoreEvent(
      event_id=row["event_id"],
      event_type=row["event_type"],
      channel=row["channel"],
      message=row.get("message"),
      severity=row.get("severity"),
      severity_hint=row.get("severity_hint"),
      sentiment=row.get("sentiment"),
      status=row["status"],
      requires_response=bool(row["requires_response"]),
      confidence=row.get("confidence"),
      predicted_type=row.get("predicted_type"),
      timestamp=row.get("timestamp"),
    )

  def _event_to_dict(self, event: StoreEvent) -> dict:
    return {
      "event_id": event.event_id,
      "event_type": event.event_type,
      "channel": event.channel,
      "message": event.message,
      "severity": event.severity,
      "severity_hint": event.severity_hint,
      "sentiment": event.sentiment,
      "status": event.status,
      "requires_response": event.requires_response,
      "confidence": event.confidence,
      "predicted_type": event.predicted_type,
      "timestamp": event.timestamp,
    }
