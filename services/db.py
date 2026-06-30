from database.base import DatabaseAdapter
from models import crud
from models.entities import AnalysisRecord, StoreEvent
from models.interfaces.analysis_repository import AnalysisRepository
from models.interfaces.event_repository import EventRepository
from utils.logger import db_logger


class DbService:
  def __init__(
    self,
    adapter: DatabaseAdapter,
    event_repository: EventRepository,
    analysis_repository: AnalysisRepository,
  ) -> None:
    self._adapter = adapter
    self._event_repository = event_repository
    self._analysis_repository = analysis_repository

  def insert_event(self, event: StoreEvent) -> StoreEvent:
    db_logger.info("Insert event: %s", event.event_id)
    return crud.insert_event(self._event_repository, event)

  def update_event(self, event: StoreEvent) -> StoreEvent:
    db_logger.info("Update event: %s", event.event_id)
    return crud.update_event(self._event_repository, event)

  def get_event(self, event_id: str) -> StoreEvent | None:
    return crud.get_event(self._event_repository, event_id)

  def get_events(self) -> list[StoreEvent]:
    return crud.get_events(self._event_repository)

  def update_analysis(self, analysis: AnalysisRecord) -> AnalysisRecord:
    db_logger.info("Update analysis: %s", analysis.event_id)
    return crud.update_analysis(self._analysis_repository, analysis)

  def health_check(self, llm_provider: str, kafka_topic: str) -> dict:
    return {
      "status": "ok",
      "events_count": self._event_repository.count(),
      "docs_count": self._adapter.count_documents(),
      "llm_provider": llm_provider,
      "kafka_topic": kafka_topic,
    }
