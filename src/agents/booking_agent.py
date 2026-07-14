import re
from dateparser.search import search_dates
from src.graph.state import SchedulerState
from src.tools.calendar_tools import check_availability, reserve_slot
from src.tools.notification import send_booking_notification
from src.tools.validator import (
    normalize_date,
    normalize_time,
    is_valid_email,
)

class BookingAgent:
    def _extract_email(self, text: str):
        match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+",text,)
        if match:
            return match.group()
        return None
    def _extract_date_time(self, text: str):
        date = None
        time = None
        matches = search_dates(
            text,
            settings={
                "PREFER_DATES_FROM": "future",
            },
        )
        if not matches:
            return date, time

        for _, parsed in matches:
            if date is None:
                date = parsed.strftime("%Y-%m-%d")
            if (
                parsed.hour != 0
                or parsed.minute != 0
            ):
                time = parsed.strftime("%H:%M")
        return date, time
    def _extract_details(self, state: SchedulerState):
        details = {
            "date": state.get("date") or "",
            "time": state.get("time") or "",
            "email": state.get("email") or "",
        }
        text = state["user_input"].strip()
        extracted_date, extracted_time = self._extract_date_time(text)
        extracted_email = self._extract_email(text)
        if extracted_date:
            details["date"] = extracted_date
        if extracted_time:
            details["time"] = extracted_time
        if extracted_email:
            details["email"] = extracted_email
        return details
    def _validate_details(self, details):
        if details["date"]:
            details["date"] = normalize_date(details["date"])
        if details["time"]:
            details["time"] = normalize_time(details["time"])
        missing_fields = []
        if not details["date"]:
            missing_fields.append("date")

        if not details["time"]:
            missing_fields.append("time")
        if not is_valid_email(details["email"]):
            missing_fields.append("email")
        return details, missing_fields

    def process(self, state: SchedulerState):
        details = self._extract_details(state)
        details, missing_fields = self._validate_details(details)
        state["date"] = details["date"]
        state["time"] = details["time"]
        state["email"] = details["email"]
        state["missing_fields"] = missing_fields
        if missing_fields:
            state["booking_status"]= "pending"
            state["response"] = (f"Please provide the following: {', '.join(missing_fields)}." )
            return state

        available =check_availability.invoke(
            {
                "date": details["date"],
                "time": details["time"],
            }
        )
        if not available:
            state["booking_status"] = "unavailable"
            state["response"] = (
                f"The slot on {details['date']} at {details['time']} is already booked.\n\n"
                "Would you like another time or date?"
            )
            return state
        reserved = reserve_slot.invoke(
            {
                "date": details["date"],
                "time": details["time"],
                "email": details["email"],
            }
        )
        if not reserved:
            state["booking_status"] = "failed"
            state["response"] = (
                "Something went wrong while reserving the appointment."
            )
            return state
        notification = send_booking_notification.invoke(
            {
                "email": details["email"],
                "date": details["date"],
                "time": details["time"],
            }
        )
        state["booking_status"] = "confirmed"
        if notification["success"]:
            state["response"] = (
                f"Your appointment has been booked for "
                f"{details['date']} at {details['time']}."
            )
        else:
            state["response"] = (
                "Your appointment was booked successfully, "
                "but the notification could not be sent."
            )
        return state