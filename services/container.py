from config import Config
from database.factory import create_database_adapter
from models.interfaces.analysis_repository import AnalysisRepository
from models.interfaces.event_repository import EventRepository
from models.repositories.analysis_repository import AnalysisRepositoryImpl
from models.repositories.event_repository import EventRepositoryImpl
from services.analysis_service import AnalysisService
from services.chat_service import ChatService
from services.db import DbService
from services.event_service import EventService
from services.health_service import HealthService
from services.ingest_service import IngestService
from services.kafka_producer import KafkaProducerService
from services.llm_client import LlmClientService
from services.rag_service import RagService
from services.report_service import ReportService
from services.tasks_service import TasksService


def create_event_repository(adapter) -> EventRepository:
  return EventRepositoryImpl(adapter)


def create_analysis_repository(adapter) -> AnalysisRepository:
  return AnalysisRepositoryImpl(adapter)


def create_db_service(
  adapter,
  event_repository: EventRepository,
  analysis_repository: AnalysisRepository,
) -> DbService:
  return DbService(
    adapter=adapter,
    event_repository=event_repository,
    analysis_repository=analysis_repository,
  )


def create_rag_service(config: Config) -> RagService:
  return RagService(config)


def create_kafka_producer(config: Config) -> KafkaProducerService:
  return KafkaProducerService(config)


def create_llm_client(config: Config, rag_service: RagService) -> LlmClientService:
  return LlmClientService(
    rag_service=rag_service,
    api_key=config.LLM_API_KEY,
    provider=config.LLM_PROVIDER,
  )


def create_health_service(db_service: DbService, rag_service: RagService, config: Config) -> HealthService:
  return HealthService(
    db_service=db_service,
    rag_service=rag_service,
    llm_provider=config.LLM_PROVIDER,
    kafka_topic=config.KAFKA_TOPIC,
  )


def create_event_service(db_service: DbService) -> EventService:
  return EventService(db_service=db_service)


def create_ingest_service(
  db_service: DbService,
  event_repository: EventRepository,
  kafka_producer: KafkaProducerService,
) -> IngestService:
  return IngestService(
    db_service=db_service,
    event_repository=event_repository,
    kafka_producer=kafka_producer,
  )


def create_analysis_service(db_service: DbService, analysis_repository: AnalysisRepository) -> AnalysisService:
  return AnalysisService(db_service=db_service, analysis_repository=analysis_repository)


def create_report_service(db_service: DbService, llm_client: LlmClientService) -> ReportService:
  return ReportService(db_service=db_service, llm_client=llm_client)


def create_tasks_service(db_service: DbService, llm_client: LlmClientService) -> TasksService:
  return TasksService(db_service=db_service, llm_client=llm_client)


def create_chat_service(db_service: DbService, llm_client: LlmClientService) -> ChatService:
  return ChatService(db_service=db_service, llm_client=llm_client)
