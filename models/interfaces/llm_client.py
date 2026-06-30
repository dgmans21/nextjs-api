from abc import ABC, abstractmethod

from models.entities import StoreEvent


class LLMClient(ABC):
  @abstractmethod
  def generate_report(self, event: StoreEvent) -> str:
    pass

  @abstractmethod
  def generate_tasks(self, event: StoreEvent) -> str:
    pass

  @abstractmethod
  def chat(self, question: str, event_id: str | None = None) -> tuple[str, list[str]]:
    pass
