from abc import ABC, abstractmethod

from models.entities import AnalysisRecord, StoreEvent


class EventRepository(ABC):
  @abstractmethod
  def find_all(self) -> list[StoreEvent]:
    pass

  @abstractmethod
  def find_by_id(self, event_id: str) -> StoreEvent | None:
    pass

  @abstractmethod
  def count(self) -> int:
    pass

  @abstractmethod
  def create(self, event: StoreEvent) -> StoreEvent:
    pass

  @abstractmethod
  def update(self, event: StoreEvent) -> StoreEvent:
    pass

  @abstractmethod
  def delete(self, event_id: str) -> bool:
    pass
