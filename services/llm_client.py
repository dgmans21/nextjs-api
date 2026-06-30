from models.entities import StoreEvent
from models.interfaces.llm_client import LLMClient
from services.rag_service import RagService
from utils.logger import llm_logger


class LlmClientService(LLMClient):
  def __init__(self, rag_service: RagService, api_key: str, provider: str) -> None:
    self._rag_service = rag_service
    self._api_key = api_key
    self._provider = provider
    self._mock_mode = not bool(api_key)

  @property
  def mock_mode(self) -> bool:
    return self._mock_mode

  def generate_report(self, event: StoreEvent) -> str:
    llm_logger.info("generate_report: %s (mock=%s)", event.event_id, self._mock_mode)
    context = self._rag_service.load_all_snippets()
    if self._mock_mode:
      return self._mock_report(event, context)
    return self._mock_report(event, context)

  def generate_tasks(self, event: StoreEvent) -> str:
    llm_logger.info("generate_tasks: %s (mock=%s)", event.event_id, self._mock_mode)
    if self._mock_mode:
      return self._mock_tasks(event)
    return self._mock_tasks(event)

  def chat(self, question: str, event_id: str | None = None) -> tuple[str, list[str]]:
    llm_logger.info("chat: event_id=%s (mock=%s)", event_id, self._mock_mode)
    sources = self._rag_service.search(question)
    source_names = [source.split(":", 1)[0] for source in sources]

    if sources:
      body = sources[0].split(":", 1)[-1].strip()
      answer = f"운영 문서 기준 답변: {body}"
    else:
      answer = f"mock 답변: \"{question}\" 질문은 운영 매뉴얼 확인이 필요합니다."

    return answer, source_names

  def _mock_report(self, event: StoreEvent, context: list[str]) -> str:
    manual_hint = context[0][:120] if context else "운영 매뉴얼"
    return (
      f"[{self._provider}] 사건 {event.event_id} 보고서\n"
      f"- 유형: {event.event_type}\n"
      f"- 채널: {event.channel}\n"
      f"- 메시지: {event.message or '없음'}\n"
      f"- 참고 문서: {manual_hint}"
    )

  def _mock_tasks(self, event: StoreEvent) -> str:
    return (
      f"1. {event.event_id} 고객 메시지 확인\n"
      f"2. {event.channel} 채널 담당자 배정\n"
      f"3. {event.event_type} 유형 표준 응대 절차 적용\n"
      f"4. 처리 결과 고객 안내 및 상태 업데이트"
    )
