from models.entities import AnalysisRecord, StoreEvent
from models.interfaces.analysis_repository import AnalysisRepository
from models.interfaces.event_repository import EventRepository


def insert_event(event_repository: EventRepository, event: StoreEvent) -> StoreEvent:
  return event_repository.create(event)


def update_event(event_repository: EventRepository, event: StoreEvent) -> StoreEvent:
  return event_repository.update(event)


def get_event(event_repository: EventRepository, event_id: str) -> StoreEvent | None:
  return event_repository.find_by_id(event_id)


def get_events(event_repository: EventRepository) -> list[StoreEvent]:
  return event_repository.find_all()


def update_analysis(analysis_repository: AnalysisRepository, analysis: AnalysisRecord) -> AnalysisRecord:
  existing = analysis_repository.find_by_event_id(analysis.event_id)
  if existing is None:
    return analysis_repository.create(analysis)
  return analysis_repository.update(analysis)
