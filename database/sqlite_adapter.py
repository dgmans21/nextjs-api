import sqlite3
from pathlib import Path
from typing import Any

from database.base import DatabaseAdapter
from utils.logger import db_logger


class SQLiteAdapter(DatabaseAdapter):
  def __init__(self, database_path: str) -> None:
    self._database_path = database_path
    self._connection: sqlite3.Connection | None = None

  def connect(self) -> None:
    Path(self._database_path).parent.mkdir(parents=True, exist_ok=True)
    self._connection = sqlite3.connect(self._database_path, check_same_thread=False)
    self._connection.row_factory = sqlite3.Row
    db_logger.info("SQLite connected: %s", self._database_path)

  def close(self) -> None:
    if self._connection is not None:
      self._connection.close()
      self._connection = None
      db_logger.info("SQLite connection closed")

  def initialize_schema(self) -> None:
    self._execute(
      """
      CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        channel TEXT NOT NULL,
        message TEXT,
        severity TEXT,
        severity_hint TEXT,
        sentiment TEXT,
        status TEXT NOT NULL,
        requires_response INTEGER NOT NULL,
        confidence REAL,
        predicted_type TEXT,
        timestamp TEXT
      )
      """
    )
    self._execute(
      """
      CREATE TABLE IF NOT EXISTS analyses (
        event_id TEXT PRIMARY KEY,
        predicted_type TEXT,
        sentiment TEXT,
        severity TEXT,
        confidence REAL,
        source TEXT,
        FOREIGN KEY (event_id) REFERENCES events(event_id)
      )
      """
    )
    self._execute(
      """
      CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL
      )
      """
    )
    db_logger.info("SQLite schema initialized")

  def fetch_all_events(self) -> list[dict[str, Any]]:
    return self._fetchall(
      """
      SELECT event_id, event_type, channel, message, severity, severity_hint,
             sentiment, status, requires_response, confidence, predicted_type, timestamp
      FROM events
      ORDER BY event_id
      """
    )

  def fetch_event_by_id(self, event_id: str) -> dict[str, Any] | None:
    return self._fetchone(
      """
      SELECT event_id, event_type, channel, message, severity, severity_hint,
             sentiment, status, requires_response, confidence, predicted_type, timestamp
      FROM events
      WHERE event_id = ?
      """,
      (event_id,),
    )

  def count_events(self) -> int:
    row = self._fetchone("SELECT COUNT(*) AS total FROM events")
    return int(row["total"]) if row else 0

  def insert_event(self, data: dict[str, Any]) -> None:
    self._execute(
      """
      INSERT INTO events (
        event_id, event_type, channel, message, severity, severity_hint,
        sentiment, status, requires_response, confidence, predicted_type, timestamp
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      """,
      (
        data["event_id"],
        data["event_type"],
        data["channel"],
        data.get("message"),
        data.get("severity"),
        data.get("severity_hint"),
        data.get("sentiment"),
        data["status"],
        1 if data["requires_response"] else 0,
        data.get("confidence"),
        data.get("predicted_type"),
        data.get("timestamp"),
      ),
    )

  def update_event(self, data: dict[str, Any]) -> None:
    self._execute(
      """
      UPDATE events
      SET event_type = ?, channel = ?, message = ?, severity = ?, severity_hint = ?,
          sentiment = ?, status = ?, requires_response = ?, confidence = ?,
          predicted_type = ?, timestamp = ?
      WHERE event_id = ?
      """,
      (
        data["event_type"],
        data["channel"],
        data.get("message"),
        data.get("severity"),
        data.get("severity_hint"),
        data.get("sentiment"),
        data["status"],
        1 if data["requires_response"] else 0,
        data.get("confidence"),
        data.get("predicted_type"),
        data.get("timestamp"),
        data["event_id"],
      ),
    )

  def delete_event(self, event_id: str) -> None:
    self._execute("DELETE FROM events WHERE event_id = ?", (event_id,))

  def fetch_analysis_by_event_id(self, event_id: str) -> dict[str, Any] | None:
    return self._fetchone(
      """
      SELECT event_id, predicted_type, sentiment, severity, confidence, source
      FROM analyses
      WHERE event_id = ?
      """,
      (event_id,),
    )

  def insert_analysis(self, data: dict[str, Any]) -> None:
    self._execute(
      """
      INSERT INTO analyses (event_id, predicted_type, sentiment, severity, confidence, source)
      VALUES (?, ?, ?, ?, ?, ?)
      """,
      (
        data["event_id"],
        data.get("predicted_type"),
        data.get("sentiment"),
        data.get("severity"),
        data.get("confidence"),
        data.get("source"),
      ),
    )

  def update_analysis(self, data: dict[str, Any]) -> None:
    self._execute(
      """
      UPDATE analyses
      SET predicted_type = ?, sentiment = ?, severity = ?, confidence = ?, source = ?
      WHERE event_id = ?
      """,
      (
        data.get("predicted_type"),
        data.get("sentiment"),
        data.get("severity"),
        data.get("confidence"),
        data.get("source"),
        data["event_id"],
      ),
    )

  def delete_analysis(self, event_id: str) -> None:
    self._execute("DELETE FROM analyses WHERE event_id = ?", (event_id,))

  def count_analyses(self) -> int:
    row = self._fetchone("SELECT COUNT(*) AS total FROM analyses")
    return int(row["total"]) if row else 0

  def count_documents(self) -> int:
    row = self._fetchone("SELECT COUNT(*) AS total FROM documents")
    return int(row["total"]) if row else 0

  def _execute(self, query: str, params: tuple[Any, ...] | None = None) -> None:
    connection = self._require_connection()
    connection.execute(query, params or ())
    connection.commit()

  def _fetchone(self, query: str, params: tuple[Any, ...] | None = None) -> dict[str, Any] | None:
    connection = self._require_connection()
    cursor = connection.execute(query, params or ())
    row = cursor.fetchone()
    return dict(row) if row is not None else None

  def _fetchall(self, query: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
    connection = self._require_connection()
    cursor = connection.execute(query, params or ())
    return [dict(row) for row in cursor.fetchall()]

  def _require_connection(self) -> sqlite3.Connection:
    if self._connection is None:
      raise RuntimeError("Database connection is not open.")
    return self._connection
