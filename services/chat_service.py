from schemas.chat import ChatRequestSchema, ChatResponseSchema
from services.db import DbService
from utils.exceptions import NotFoundAppError
from services.llm_client import LlmClientService


class ChatService:
  def __init__(self, db_service: DbService, llm_client: LlmClientService) -> None:
    self._db_service = db_service
    self._llm_client = llm_client
    self._request_schema = ChatRequestSchema()
    self._response_schema = ChatResponseSchema()

  def chat(self, payload: dict) -> dict:
    data = self._request_schema.load(payload)
    event_id = data.get("event_id")
    if event_id and self._db_service.get_event(event_id) is None:
      raise NotFoundAppError(f"Event not found: {event_id}")

    answer, sources = self._llm_client.chat(data["question"], event_id)
    response = {"answer": answer, "sources": sources or None}
    return self._response_schema.dump(response)
