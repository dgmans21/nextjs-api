from flask import Blueprint, jsonify, request

from schemas.event import EventIdParamSchema
from services.event_service import EventService
from services.ingest_service import IngestService
from utils.logger import api_logger


def create_event_blueprint(event_service: EventService, ingest_service: IngestService) -> Blueprint:
  blueprint = Blueprint("events", __name__)
  param_schema = EventIdParamSchema()

  @blueprint.get("/events")
  def list_events():
    api_logger.info("GET /events")
    return jsonify(event_service.list_events())

  @blueprint.get("/events/<string:event_id>")
  def get_event(event_id: str):
    api_logger.info("GET /events/%s", event_id)
    param_schema.load({"event_id": event_id})
    return jsonify(event_service.get_event(event_id))

  @blueprint.post("/ingest")
  def ingest_event():
    api_logger.info("POST /ingest")
    payload = request.get_json(silent=True) or {}
    return jsonify(ingest_service.ingest(payload)), 201

  return blueprint
