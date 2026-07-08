import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _resolve_path(value: str, base: Path = BASE_DIR) -> Path:
  path = Path(value)
  if not path.is_absolute():
    path = base / path
  return path.resolve()


class Config:
  FLASK_ENV = os.getenv("FLASK_ENV", "development")
  DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
  HOST = os.getenv("FLASK_HOST", "127.0.0.1")
  PORT = int(os.getenv("FLASK_PORT", "5000"))

  DATABASE_TYPE = os.getenv("DATABASE_TYPE", os.getenv("DB_TYPE", "sqlite")).lower()
  DB_TYPE = DATABASE_TYPE
  SQLITE_PATH = os.getenv("SQLITE_PATH", str(BASE_DIR / "data" / "ops.db"))

  MARIADB_HOST = os.getenv("MARIADB_HOST", "localhost")
  MARIADB_PORT = int(os.getenv("MARIADB_PORT", "3306"))
  MARIADB_USER = os.getenv("MARIADB_USER", "ops")
  MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "")
  MARIADB_DATABASE = os.getenv("MARIADB_DATABASE", "ops")

  CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
      "CORS_ORIGINS",
      "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
  ]

  LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
  LLM_API_KEY = os.getenv("LLM_API_KEY", "")
  KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "ops-events")
  KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
  KAFKA_ENABLED = os.getenv("KAFKA_ENABLED", "0") == "1"
  DOCS_DIR = os.getenv("DOCS_DIR", str(BASE_DIR / "data" / "docs"))
  LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

  MYKAFKAKERAS_DIR = _resolve_path(
    os.getenv("MYKAFKAKERAS_DIR", str(BASE_DIR.parent / "mykafkakeras"))
  )
  KERAS_ENABLED = os.getenv("KERAS_ENABLED", "1") == "1"
  KERAS_MODEL_PATH = _resolve_path(
    os.getenv(
      "KERAS_MODEL_PATH",
      str(MYKAFKAKERAS_DIR / "models" / "case.1" / "event_type_v1.keras"),
    )
  )
  KERAS_CLASS_MAP_PATH = _resolve_path(
    os.getenv(
      "KERAS_CLASS_MAP_PATH",
      str(MYKAFKAKERAS_DIR / "models" / "case.1" / "class_map.json"),
    )
  )

  # Hugging Face (klue/bert-base) — mykafkakeras/models/case.2/
  INFERENCE_BACKEND = os.getenv("INFERENCE_BACKEND", "auto").lower()
  HF_ENABLED = os.getenv("HF_ENABLED", "1") == "1"
  HF_MODEL_DIR = _resolve_path(
    os.getenv(
      "HF_MODEL_DIR",
      str(MYKAFKAKERAS_DIR / "models" / "case.2" / "hf-klue-bert-v1"),
    )
  )
  HF_MAX_LENGTH = int(os.getenv("HF_MAX_LENGTH", "128"))
