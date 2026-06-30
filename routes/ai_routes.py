from flask import Blueprint, jsonify, request

from schemas.event import EventIdParamSchema
from services.analysis_service import AnalysisService
from services.chat_service import ChatService
from services.report_service import ReportService
from services.tasks_service import TasksService
from utils.logger import api_logger


def create_ai_blueprint(
  analysis_service: AnalysisService,
  report_service: ReportService,
  tasks_service: TasksService,
  chat_service: ChatService,
) -> Blueprint:
  blueprint = Blueprint("ai", __name__)
  param_schema = EventIdParamSchema()

  @blueprint.get("/events/<string:event_id>/analysis")
  def get_analysis(event_id: str):
    api_logger.info("GET /events/%s/analysis", event_id)
    param_schema.load({"event_id": event_id})
    return jsonify(analysis_service.get_analysis(event_id))

  @blueprint.post("/events/<string:event_id>/report")
  def generate_report(event_id: str):
    api_logger.info("POST /events/%s/report", event_id)
    param_schema.load({"event_id": event_id})
    return jsonify(report_service.generate_report(event_id))

  @blueprint.post("/events/<string:event_id>/tasks")
  def generate_tasks(event_id: str):
    api_logger.info("POST /events/%s/tasks", event_id)
    param_schema.load({"event_id": event_id})
    return jsonify(tasks_service.generate_tasks(event_id))

  @blueprint.post("/chat")
  def chat():
    api_logger.info("POST /chat")
    payload = request.get_json(silent=True) or {}
    return jsonify(chat_service.chat(payload))

  return blueprint
