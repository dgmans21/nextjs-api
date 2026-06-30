from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class StoreEvent:
  event_id: str
  event_type: str
  channel: str
  status: str
  requires_response: bool
  message: str | None = None
  severity: str | None = None
  severity_hint: str | None = None
  sentiment: str | None = None
  confidence: float | None = None
  predicted_type: str | None = None
  timestamp: str | None = None

  def to_dict(self) -> dict[str, Any]:
    payload = asdict(self)
    return {key: value for key, value in payload.items() if value is not None}


@dataclass
class AnalysisRecord:
  event_id: str
  predicted_type: str | None = None
  sentiment: str | None = None
  severity: str | None = None
  confidence: float | None = None
  source: str | None = None

  def to_dict(self) -> dict[str, Any]:
    payload = asdict(self)
    return {key: value for key, value in payload.items() if value is not None}
