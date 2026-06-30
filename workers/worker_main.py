"""
Independent worker process skeleton.

Run separately from Flask:
  python -m workers.worker_main
"""

import logging
import time

from config import Config
from utils.logger import kafka_logger

logger = logging.getLogger(__name__)


def run_worker(config: Config) -> None:
  kafka_logger.info("Worker started (Kafka consumer not implemented yet).")
  kafka_logger.info("Kafka topic placeholder: %s", config.KAFKA_TOPIC)

  while True:
    kafka_logger.debug("Worker heartbeat")
    time.sleep(5)


if __name__ == "__main__":
  logging.basicConfig(level=Config.LOG_LEVEL)
  run_worker(Config())
