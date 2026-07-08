import os

os.environ.setdefault("PYTHONUTF8", "1")

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

from config import Config
from openapi.spec import OPENAPI_SPEC
from routes import create_ai_blueprint, create_event_blueprint, create_health_blueprint
from services.container import (
  create_analysis_repository,
  create_analysis_service,
  create_chat_service,
  create_database_adapter,
  create_db_service,
  create_event_repository,
  create_event_service,
  create_health_service,
  create_ingest_service,
  create_kafka_producer,
  create_llm_client,
  create_rag_service,
  create_report_service,
  create_tasks_service,
)
from services.model_inference import init_inference
from services.seed import seed_events
from utils import api_logger, register_error_handlers
from utils.logger import db_logger, kafka_logger, llm_logger


SWAGGER_UI_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Ops API Docs</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.onload = () => {
        SwaggerUIBundle({
          url: '/openapi.json',
          dom_id: '#swagger-ui'
        });
      };
    </script>
  </body>
</html>
"""


def configure_logging(config: Config) -> None:
  level_name = config.LOG_LEVEL.upper()
  level = getattr(__import__("logging"), level_name, 20)
  for logger in (api_logger, db_logger, kafka_logger, llm_logger):
    logger.setLevel(level)


def create_app(config: Config | None = None) -> Flask:
  app_config = config or Config()
  configure_logging(app_config)
  init_inference(app_config)

  app = Flask(__name__)
  app.config.from_object(app_config)
  CORS(app, resources={r"/*": {"origins": app_config.CORS_ORIGINS}})
  register_error_handlers(app)

  adapter = create_database_adapter(app_config)
  adapter.connect()
  adapter.initialize_schema()

  event_repository = create_event_repository(adapter)
  analysis_repository = create_analysis_repository(adapter)
  seed_events(event_repository)

  rag_service = create_rag_service(app_config)
  kafka_producer = create_kafka_producer(app_config)
  llm_client = create_llm_client(app_config, rag_service)

  db_service = create_db_service(adapter, event_repository, analysis_repository)
  event_service = create_event_service(db_service)
  health_service = create_health_service(db_service, rag_service, app_config)
  ingest_service = create_ingest_service(db_service, event_repository, kafka_producer)
  analysis_service = create_analysis_service(db_service, analysis_repository)
  report_service = create_report_service(db_service, llm_client)
  tasks_service = create_tasks_service(db_service, llm_client)
  chat_service = create_chat_service(db_service, llm_client)

  app.register_blueprint(create_health_blueprint(health_service))
  app.register_blueprint(create_event_blueprint(event_service, ingest_service))
  app.register_blueprint(
    create_ai_blueprint(analysis_service, report_service, tasks_service, chat_service)
  )
  app.extensions["database_adapter"] = adapter
  app.extensions["kafka_producer"] = kafka_producer

  @app.get("/openapi.json")
  def openapi_json():
    return jsonify(OPENAPI_SPEC)

  @app.get("/docs")
  def swagger_ui():
    return render_template_string(SWAGGER_UI_TEMPLATE)

  api_logger.info("Flask app initialized")
  return app


if __name__ == "__main__":
  application = create_app()
  application.run(
    host=application.config["HOST"],
    port=application.config["PORT"],
    debug=application.config["DEBUG"],
  )
