import json
from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.llm import llm
from src.graph.state import SchedulerState
from src.prompts.booking_prompt import BOOKING_PROMPT
from src.tools.calendar_tools import check_availability, reserve_slot
from src.tools.notification import send_booking_notification
from src.tools.validator import (
    normalize_date,
    normalize_time,
    is_valid_email,
)

class BookingAgent:
    def __init__(self):
        self.llm = llm
    def _extract_details(self, user_input: str) -> dict:
        response = self.llm.invoke(
            [
                SystemMessage(content=BOOKING_PROMPT),
                HumanMessage(content=user_input),
            ]
        )
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "date": "",
                "time": "",
                "email": "",
            }
    def _validate_details(self, details: dict):
        details["date"] = normalize_date(details["date"])
        details["time"] = normalize_time(details["time"])
        missing_fields = []
        if not details["date"]:
            missing_fields.append("date")
        if not details["time"]:
            missing_fields.append("time")
        email = details["email"]
        if not email or not is_valid_email(email):
            missing_fields.append("email")
        return details, missing_fields
    def process(self, state: SchedulerState):
        details = self._extract_details(state["user_input"])
        details, missing_fields = self._validate_details(details)

        date = details["date"]
        time = details["time"]
        email = details["email"]

        state["date"] = date
        state["time"] = time
        state["email"] = email
        state["missing_fields"] = missing_fields
        if missing_fields:
            state["booking_status"] = "pending"
            state["response"] = (
                f"Please provide the following: {', '.join(missing_fields)}."
            )
            return state
        available = check_availability.invoke(
            {
                "date": date,
                "time": time,
            }
        )
        if not available:
            state["booking_status"] = "unavailable"
            state["response"] = (
                f"The requested slot on {date} at {time} is already booked.\n\n"
                "Would you like to choose another time or a different date?"
            )
            return state
        reserved = reserve_slot.invoke(
            {
                "date": date,
                "time": time,
                "email": email,
            }
        )
        if not reserved:
            state["booking_status"] = "failed"
            state["response"] = (
                "Something went wrong while reserving your appointment."
            )
            return state
        notification = send_booking_notification.invoke(
            {
                "email": email,
                "date": date,
                "time": time,
            }
        )
        if not notification["success"]:
            state["booking_status"] = "confirmed"
            state["response"] = (
                "Your appointment has been booked successfully, "
                "but the confirmation notification could not be sent."
            )
            return state

        state["booking_status"] = "confirmed"
        state["response"] = (
            f"Your appointment has been booked for {date} at {time}."
        )

        return state
        