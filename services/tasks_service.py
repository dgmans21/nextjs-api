from services.db import DbService
from services.llm_client import LlmClientService
from utils.exceptions import NotFoundAppError


class TasksService:
  def __init__(self, db_service: DbService, llm_client: LlmClientService) -> None:
    self._db_service = db_service
    self._llm_client = llm_client

  def generate_tasks(self, event_id: str) -> dict:
    event = self._db_service.get_event(event_id)
    if event is None:
      raise NotFoundAppError(f"Event not found: {event_id}")

    result = self._llm_client.generate_tasks(event)
    return {"event_id": event_id, "result": result}
