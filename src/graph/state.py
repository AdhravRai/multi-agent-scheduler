from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class SchedulerState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str
    date: str | None
    time: str | None
    email: str | None
    missing_fields: list[str]
    booking_status: str
    response: str
    user_input: str