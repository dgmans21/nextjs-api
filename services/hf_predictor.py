import os
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")

from utils.logger import api_logger

_tokenizer = None
_model = None
_id2label: dict[int, str] | None = None
_device = None


def is_ready() -> bool:
  return _model is not None and _tokenizer is not None and _id2label is not None


def init_hf_predictor(model_dir: Path, max_length: int = 128) -> bool:
  global _tokenizer, _model, _id2label, _device

  config_path = model_dir / "config.json"
  if not config_path.is_file():
    api_logger.warning("HF model config not found: %s", config_path)
    return False

  try:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
  except ImportError as error:
    api_logger.warning("HF dependencies missing (transformers/torch): %s", error)
    return False

  try:
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.eval()

    id2label_raw = model.config.id2label
    id2label = {int(key): value for key, value in id2label_raw.items()}
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    _tokenizer = tokenizer
    _model = model
    _id2label = id2label
    _device = device
    _tokenizer.model_max_length = max_length
  except Exception as error:
    api_logger.exception("Failed to load HF predictor: %s", error)
    _tokenizer = None
    _model = None
    _id2label = None
    _device = None
    return False

  api_logger.info("HF predictor loaded: %s (device=%s)", model_dir, _device)
  return True


def predict_message(message: str, max_length: int = 128) -> dict | None:
  if not is_ready() or not message.strip():
    return None

  import torch

  inputs = _tokenizer(
    message,
    return_tensors="pt",
    truncation=True,
    padding=True,
    max_length=max_length,
  )
  inputs = {key: value.to(_device) for key, value in inputs.items()}

  with torch.no_grad():
    logits = _model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)[0]

  idx = int(torch.argmax(probs).item())
  return {
    "event_type": _id2label[idx],
    "confidence": float(probs[idx].item()),
  }
