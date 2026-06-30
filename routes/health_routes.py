from flask import Blueprint, jsonify

from services.health_service import HealthService
from utils.logger import api_logger


def create_health_blueprint(health_service: HealthService) -> Blueprint:
  blueprint = Blueprint("health", __name__)

  @blueprint.get("/health")
  def health():
    api_logger.info("GET /health")
    return jsonify(health_service.get_health())

  return blueprint
