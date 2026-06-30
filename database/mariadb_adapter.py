from typing import Any

from database.base import DatabaseAdapter
from utils.logger import db_logger


class MariaDBAdapter(DatabaseAdapter):
  def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
    self._host = host
    self._port = port
    self._user = user
    self._password = password
    self._database = database

  def connect(self) -> None:
    db_logger.error("MariaDB adapter is not implemented yet")
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def close(self) -> None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def initialize_schema(self) -> None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def fetch_all_events(self) -> list[dict[str, Any]]:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def fetch_event_by_id(self, event_id: str) -> dict[str, Any] | None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def count_events(self) -> int:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def insert_event(self, data: dict[str, Any]) -> None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def update_event(self, data: dict[str, Any]) -> None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def delete_event(self, event_id: str) -> None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def fetch_analysis_by_event_id(self, event_id: str) -> dict[str, Any] | None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def insert_analysis(self, data: dict[str, Any]) -> None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def update_analysis(self, data: dict[str, Any]) -> None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def delete_analysis(self, event_id: str) -> None:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def count_analyses(self) -> int:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")

  def count_documents(self) -> int:
    raise NotImplementedError("MariaDB adapter is not implemented yet.")
