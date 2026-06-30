from abc import ABC, abstractmethod

from models.entities import AnalysisRecord


class AnalysisRepository(ABC):
  @abstractmethod
  def find_by_event_id(self, event_id: str) -> AnalysisRecord | None:
    pass

  @abstractmethod
  def create(self, analysis: AnalysisRecord) -> AnalysisRecord:
    pass

  @abstractmethod
  def update(self, analysis: AnalysisRecord) -> AnalysisRecord:
    pass

  @abstractmethod
  def delete(self, event_id: str) -> bool:
    pass

  @abstractmethod
  def count(self) -> int:
    pass
