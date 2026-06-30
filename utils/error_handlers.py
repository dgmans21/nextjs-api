from flask import Flask, jsonify
from marshmallow import ValidationError

from utils.exceptions import AppError
from utils.logger import api_logger


def register_error_handlers(app: Flask) -> None:
  @app.errorhandler(AppError)
  def handle_app_error(error: AppError):
    api_logger.warning("App error: %s", error.message)
    return jsonify(_error_payload(error.code, error.message, error.details)), error.status_code

  @app.errorhandler(ValidationError)
  def handle_validation_error(error: ValidationError):
    api_logger.warning("Schema validation failed: %s", error.messages)
    return jsonify(_error_payload("validation_error", "Request validation failed", error.messages)), 400

  @app.errorhandler(404)
  def handle_not_found(_error):
    return jsonify(_error_payload("not_found", "Resource not found")), 404

  @app.errorhandler(405)
  def handle_method_not_allowed(_error):
    return jsonify(_error_payload("method_not_allowed", "Method not allowed")), 405

  @app.errorhandler(500)
  def handle_internal_error(error):
    api_logger.exception("Unhandled server error: %s", error)
    return jsonify(_error_payload("internal_server_error", "Internal server error")), 500


def _error_payload(code: str, message: str, details: dict | list | None = None) -> dict:
  payload = {"error": code, "message": message}
  if details:
    payload["details"] = details
  return payload
