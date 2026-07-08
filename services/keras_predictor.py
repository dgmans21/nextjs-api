import json
import os
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")

import numpy as np
import tensorflow as tf

from utils.logger import api_logger

_model = None
_index_to_label: dict[int, str] | None = None


def is_ready() -> bool:
  return _model is not None and _index_to_label is not None


def init_keras_predictor(model_path: Path, class_map_path: Path) -> bool:
  global _model, _index_to_label

  if not model_path.is_file():
    api_logger.warning("Keras model not found: %s", model_path)
    return False

  if not class_map_path.is_file():
    api_logger.warning("Keras class map not found: %s", class_map_path)
    return False

  try:
    model = tf.keras.models.load_model(model_path)
    class_map = json.loads(class_map_path.read_text(encoding="utf-8"))
    index_to_label = {int(key): value for key, value in class_map["index_to_label"].items()}
  except Exception as error:
    api_logger.exception("Failed to load Keras predictor: %s", error)
    _model = None
    _index_to_label = None
    return False

  _model = model
  _index_to_label = index_to_label
  api_logger.info("Keras predictor loaded: %s", model_path)
  return True


def predict_message(message: str) -> dict | None:
  if not is_ready() or not message.strip():
    return None

  probs = _model.predict(np.array([message], dtype=object), verbose=0)
  prob = probs[0]
  idx = int(np.argmax(prob))
  event_type = _index_to_label[idx]
  return {
    "event_type": event_type,
    "confidence": float(prob[idx]),
  }
