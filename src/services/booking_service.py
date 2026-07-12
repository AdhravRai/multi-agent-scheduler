from src.tools.validator import (
    is_valid_email,
    normalize_date,
    normalize_time,
)
class BookingService:
    def validate_booking(self,date: str,time: str,email: str,) -> dict:
        normalized_date = normalize_date(date)
        if normalized_date is None:
            return {
                "success": False,
                "message": "Invalid date.",
            }
        normalized_time = normalize_time(time)
        if normalized_time is None:
            return {
                "success": False,
                "message": "Invalid time.",
            }
        if not is_valid_email(email):
            return {
                "success": False,
                "message": "Invalid email address.",
            }
        return {
            "success": True,
            "data": {
                "date": normalized_date,
                "time": normalized_time,
                "email": email,
            },
        }
    def check_slot(self, date: str, time: str) -> dict:
        available = check_availability.invoke({
            "date": date,
            "time": time
        })
        if available:
            return {
                "success": True
            }
        return {
            "success": False,
            "message": "This slot is already booked."
        }