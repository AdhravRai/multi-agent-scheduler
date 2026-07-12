import requests
from langchain_core.tools import tool
from src.config.settings import WEBHOOK_URL

@tool
def send_booking_notification(email: str, date: str, time: str) -> dict:
    payload = {
        "email": email,
        "date": date,
        "time": time
    }
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return {
            "success": True,
            "message": "Notification sent successfully.",
            "data": payload
        }
    except requests.RequestException as exc:
        return {
            "success": False,
            "message": str(e),
            "data": None
        }