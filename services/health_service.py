from services.db import DbService
from services.rag_service import RagService


class HealthService:
  def __init__(
    self,
    db_service: DbService,
    rag_service: RagService,
    llm_provider: str,
    kafka_topic: str,
  ) -> None:
    self._db_service = db_service
    self._rag_service = rag_service
    self._llm_provider = llm_provider
    self._kafka_topic = kafka_topic

  def get_health(self) -> dict:
    payload = self._db_service.health_check(
      llm_provider=self._llm_provider,
      kafka_topic=self._kafka_topic,
    )
    payload["docs_count"] = self._rag_service.count_documents()
    return payload
