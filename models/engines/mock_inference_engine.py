from models.entities import AnalysisRecord, StoreEvent
from models.interfaces.inference_engine import InferenceEngine


class MockInferenceEngine(InferenceEngine):
  def analyze(self, event: StoreEvent) -> AnalysisRecord:
    return AnalysisRecord(
      event_id=event.event_id,
      predicted_type=event.event_type,
      sentiment="neutral",
      severity=event.severity,
      confidence=0.0,
      source="mock",
    )
