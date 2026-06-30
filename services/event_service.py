from services.db import DbService
from utils.exceptions import NotFoundAppError


class EventService:
  def __init__(self, db_service: DbService) -> None:
    self._db_service = db_service

  def list_events(self) -> dict:
    events = self._db_service.get_events()
    return {
      "count": len(events),
      "events": [event.to_dict() for event in events],
    }

  def get_event(self, event_id: str) -> dict:
    event = self._db_service.get_event(event_id)
    if event is None:
      raise NotFoundAppError(f"Event not found: {event_id}")
    return event.to_dict()
