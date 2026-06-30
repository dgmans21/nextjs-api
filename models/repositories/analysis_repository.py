from models.entities import AnalysisRecord
from models.interfaces.analysis_repository import AnalysisRepository


class AnalysisRepositoryImpl(AnalysisRepository):
  def __init__(self, adapter) -> None:
    from database.base import DatabaseAdapter

    self._adapter: DatabaseAdapter = adapter

  def find_by_event_id(self, event_id: str) -> AnalysisRecord | None:
    row = self._adapter.fetch_analysis_by_event_id(event_id)
    return self._row_to_analysis(row) if row else None

  def create(self, analysis: AnalysisRecord) -> AnalysisRecord:
    self._adapter.insert_analysis(self._analysis_to_dict(analysis))
    return analysis

  def update(self, analysis: AnalysisRecord) -> AnalysisRecord:
    self._adapter.update_analysis(self._analysis_to_dict(analysis))
    return analysis

  def delete(self, event_id: str) -> bool:
    existing = self.find_by_event_id(event_id)
    if existing is None:
      return False
    self._adapter.delete_analysis(event_id)
    return True

  def count(self) -> int:
    return self._adapter.count_analyses()

  def _row_to_analysis(self, row: dict) -> AnalysisRecord:
    return AnalysisRecord(
      event_id=row["event_id"],
      predicted_type=row.get("predicted_type"),
      sentiment=row.get("sentiment"),
      severity=row.get("severity"),
      confidence=row.get("confidence"),
      source=row.get("source"),
    )

  def _analysis_to_dict(self, analysis: AnalysisRecord) -> dict:
    return {
      "event_id": analysis.event_id,
      "predicted_type": analysis.predicted_type,
      "sentiment": analysis.sentiment,
      "severity": analysis.severity,
      "confidence": analysis.confidence,
      "source": analysis.source,
    }
