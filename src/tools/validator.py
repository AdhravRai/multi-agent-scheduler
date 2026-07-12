import re
from datetime import datetime
import dateparser

def normalize_date(date_text: str) -> str | None:
    parsed_date = dateparser.parse(
        date_text,
        settings={"PREFER_DATES_FROM": "future"},
    )
    if not parsed_date:
        return None
    return parsed_date.strftime("%Y-%m-%d")

def normalize_time(time_text: str) -> str | None:
    parsed_time = dateparser.parse(time_text)
    if not parsed_time:
        return None
    return parsed_time.strftime("%H:%M")

def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.fullmatch(pattern, email) is not None