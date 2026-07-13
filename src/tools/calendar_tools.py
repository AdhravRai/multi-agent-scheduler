from langchain_core.tools import tool

from src.database.database import db


@tool
def check_availability(date: str, time: str) -> bool:
    """Check whether the requested appointment slot is available."""
    return db.check_slot_available(date, time)


@tool
def reserve_slot(date: str, time: str, email: str) -> bool:
    """Reserve an appointment slot."""
    return db.reserve_slot(date, time, email)