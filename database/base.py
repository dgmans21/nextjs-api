from abc import ABC, abstractmethod
from typing import Any


class DatabaseAdapter(ABC):
  @abstractmethod
  def connect(self) -> None:
    pass

  @abstractmethod
  def close(self) -> None:
    pass

  @abstractmethod
  def initialize_schema(self) -> None:
    pass

  @abstractmethod
  def fetch_all_events(self) -> list[dict[str, Any]]:
    pass

  @abstractmethod
  def fetch_event_by_id(self, event_id: str) -> dict[str, Any] | None:
    pass

  @abstractmethod
  def count_events(self) -> int:
    pass

  @abstractmethod
  def insert_event(self, data: dict[str, Any]) -> None:
    pass

  @abstractmethod
  def update_event(self, data: dict[str, Any]) -> None:
    pass

  @abstractmethod
  def delete_event(self, event_id: str) -> None:
    pass

  @abstractmethod
  def fetch_analysis_by_event_id(self, event_id: str) -> dict[str, Any] | None:
    pass

  @abstractmethod
  def insert_analysis(self, data: dict[str, Any]) -> None:
    pass

  @abstractmethod
  def update_analysis(self, data: dict[str, Any]) -> None:
    pass

  @abstractmethod
  def delete_analysis(self, event_id: str) -> None:
    pass

  @abstractmethod
  def count_analyses(self) -> int:
    pass

  @abstractmethod
  def count_documents(self) -> int:
    pass
