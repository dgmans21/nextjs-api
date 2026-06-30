import json
from typing import Any

from config import Config
from utils.logger import kafka_logger


class KafkaProducerService:
  def __init__(self, config: Config) -> None:
    self._config = config
    self._producer = None

    if config.KAFKA_ENABLED:
      try:
        from kafka import KafkaProducer

        self._producer = KafkaProducer(
          bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS.split(","),
          value_serializer=lambda value: json.dumps(value, ensure_ascii=False).encode("utf-8"),
        )
        kafka_logger.info("Kafka producer connected: %s", config.KAFKA_BOOTSTRAP_SERVERS)
      except Exception as error:
        kafka_logger.warning("Kafka producer init failed: %s", error)
        self._producer = None

  def publish_event(self, event: dict[str, Any]) -> bool:
    if self._producer is None:
      kafka_logger.warning("Kafka publish skipped (producer unavailable)")
      return False

    try:
      future = self._producer.send(self._config.KAFKA_TOPIC, event)
      future.get(timeout=5)
      kafka_logger.info("Kafka published event: %s", event.get("event_id"))
      return True
    except Exception as error:
      kafka_logger.error("Kafka publish failed: %s", error)
      return False

  def close(self) -> None:
    if self._producer is not None:
      self._producer.close()
      kafka_logger.info("Kafka producer closed")
