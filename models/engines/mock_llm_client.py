from models.entities import StoreEvent
from models.interfaces.llm_client import LLMClient


class MockLLMClient(LLMClient):
  def generate_report(self, event: StoreEvent) -> str:
    return f"Mock report for {event.event_id}"

  def generate_tasks(self, event: StoreEvent) -> str:
    return f"1. Review {event.event_id}\n2. Contact customer"

  def chat(self, question: str, event_id: str | None = None) -> tuple[str, list[str]]:
    return f"Mock answer for: {question}", []
