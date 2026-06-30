from models.entities import StoreEvent
from models.interfaces.event_repository import EventRepository


SEED_EVENTS: list[StoreEvent] = [
  StoreEvent(
    event_id="evt-001",
    event_type="refund",
    channel="counter",
    message="환불 처리 지연 문의",
    severity="high",
    status="open",
    requires_response=True,
  ),
  StoreEvent(
    event_id="evt-002",
    event_type="delay",
    channel="mobile_order",
    message="픽업 대기 시간 문의",
    severity="medium",
    status="open",
    requires_response=True,
  ),
  StoreEvent(
    event_id="evt-003",
    event_type="quality",
    channel="delivery",
    message="포장 상태 불만",
    severity="medium",
    status="open",
    requires_response=True,
  ),
]


def seed_events(event_repository: EventRepository) -> None:
  if event_repository.count() > 0:
    return

  for event in SEED_EVENTS:
    event_repository.create(event)
