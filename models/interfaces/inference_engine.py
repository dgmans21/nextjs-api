from abc import ABC, abstractmethod

from models.entities import AnalysisRecord, StoreEvent


class InferenceEngine(ABC):
  @abstractmethod
  def analyze(self, event: StoreEvent) -> AnalysisRecord:
    pass
