from dataclasses import dataclass

from models.entities import StoreEvent


@dataclass
class PredictionResult:
  predicted_type: str
  severity: str
  summary: str
  confidence: float
  action_required: bool


_RULES: list[dict] = [
  {
    "keywords": ("환불", "refund"),
    "predicted_type": "refund",
    "severity": "high",
    "summary": "환불 관련 민원으로 결제·영수증 확인이 필요합니다.",
    "confidence": 0.82,
    "action_required": True,
  },
  {
    "keywords": ("대기", "지연", "delay"),
    "predicted_type": "delay",
    "severity": "medium",
    "summary": "대기/지연 문의로 현재 제조·픽업 상태 확인이 필요합니다.",
    "confidence": 0.76,
    "action_required": True,
  },
  {
    "keywords": ("품질", "포장", "quality"),
    "predicted_type": "quality",
    "severity": "medium",
    "summary": "품질/포장 불만으로 현장 확인 및 재조치 검토가 필요합니다.",
    "confidence": 0.74,
    "action_required": True,
  },
]


def predict(event: StoreEvent) -> PredictionResult:
  text = " ".join(
    filter(
      None,
      [event.message or "", event.event_type or "", event.channel or ""],
    )
  ).lower()

  for rule in _RULES:
    if any(keyword in text for keyword in rule["keywords"]):
      return PredictionResult(
        predicted_type=rule["predicted_type"],
        severity=rule["severity"],
        summary=rule["summary"],
        confidence=rule["confidence"],
        action_required=rule["action_required"],
      )

  severity = event.severity or "low"
  return PredictionResult(
    predicted_type=event.event_type or "general",
    severity=severity,
    summary="일반 문의로 기본 응대 절차를 적용합니다.",
    confidence=0.55,
    action_required=event.requires_response,
  )
