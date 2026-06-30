import logging
from typing import Literal

LoggerName = Literal["api", "database", "kafka", "llm"]


def get_logger(name: LoggerName) -> logging.Logger:
  logger = logging.getLogger(f"ops.{name}")
  if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
      logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
  return logger


api_logger = get_logger("api")
db_logger = get_logger("database")
kafka_logger = get_logger("kafka")
llm_logger = get_logger("llm")
