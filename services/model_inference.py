from dataclasses import dataclass

from config import Config
from models.entities import StoreEvent
from services import keras_predictor
from utils.logger import api_logger


@dataclass
class PredictionResult:
  predicted_type: str
  severity: str
  summary: str
  confidence: float
  action_required: bool
  source: str = "rule-based"


_TYPE_META: dict[str, dict] = {
  "refund": {
    "severity": "high",
    "summary": "환불 관련 민원으로 결제·영수증 확인이 필요합니다.",
    "action_required": True,
  },
  "delay": {
    "severity": "medium",
    "summary": "대기/지연 문의로 현재 제조·픽업 상태 확인이 필요합니다.",
    "action_required": True,
  },
  "quality": {
    "severity": "medium",
    "summary": "품질/포장 불만으로 현장 확인 및 재조치 검토가 필요합니다.",
    "action_required": True,
  },
  "order_issue": {
    "severity": "high",
    "summary": "주문/결제 오류로 거래 내역과 시스템 로그 확인이 필요합니다.",
    "action_required": True,
  },
  "complaint": {
    "severity": "medium",
    "summary": "고객 불만/민원으로 담당자 확인 및 응대가 필요합니다.",
    "action_required": True,
  },
  "safety": {
    "severity": "high",
    "summary": "안전 이슈로 즉시 현장 점검 및 위험 요소 제거가 필요합니다.",
    "action_required": True,
  },
  "inventory": {
    "severity": "medium",
    "summary": "재고 부족으로 발주·대체 메뉴 안내 검토가 필요합니다.",
    "action_required": True,
  },
  "staff_note": {
    "severity": "low",
    "summary": "직원 메모로 내부 공유 및 후속 확인이 필요합니다.",
    "action_required": False,
  },
}


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


def init_inference(config: Config) -> None:
  if not config.KERAS_ENABLED:
    api_logger.info("Keras inference disabled (KERAS_ENABLED=0)")
    return

  keras_predictor.init_keras_predictor(config.KERAS_MODEL_PATH, config.KERAS_CLASS_MAP_PATH)


def _meta_for_type(predicted_type: str) -> dict:
  return _TYPE_META.get(
    predicted_type,
    {
      "severity": "low",
      "summary": "일반 문의로 기본 응대 절차를 적용합니다.",
      "action_required": True,
    },
  )


def _from_type(predicted_type: str, confidence: float, source: str) -> PredictionResult:
  meta = _meta_for_type(predicted_type)
  return PredictionResult(
    predicted_type=predicted_type,
    severity=meta["severity"],
    summary=meta["summary"],
    confidence=confidence,
    action_required=meta["action_required"],
    source=source,
  )


def _rule_predict(text: str, event: StoreEvent) -> PredictionResult | None:
  for rule in _RULES:
    if any(keyword in text for keyword in rule["keywords"]):
      return PredictionResult(
        predicted_type=rule["predicted_type"],
        severity=rule["severity"],
        summary=rule["summary"],
        confidence=rule["confidence"],
        action_required=rule["action_required"],
        source="rule-based",
      )
  return None


def predict(event: StoreEvent) -> PredictionResult:
  message = (event.message or "").strip()
  text = " ".join(
    filter(
      None,
      [message, event.event_type or "", event.channel or ""],
    )
  ).lower()

  if keras_predictor.is_ready() and message:
    keras_result = keras_predictor.predict_message(message)
    if keras_result is not None:
      return _from_type(
        keras_result["event_type"],
        keras_result["confidence"],
        "keras",
      )

  rule_result = _rule_predict(text, event)
  if rule_result is not None:
    return rule_result

  severity = event.severity or "low"
  return PredictionResult(
    predicted_type=event.event_type or "general",
    severity=severity,
    summary="일반 문의로 기본 응대 절차를 적용합니다.",
    confidence=0.55,
    action_required=event.requires_response,
    source="rule-based",
  )
