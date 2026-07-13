from src.tools.calendar_tools import check_availability, reserve_slot
from src.tools.notification import send_booking_notification

print("Check Availability:")
print(
    check_availability.invoke(
        {
            "date": "2026-07-20",
            "time": "10:00",
        }
    )
)

print("\nReserve Slot:")
print(
    reserve_slot.invoke(
        {
            "date": "2026-07-20",
            "time": "10:00",
            "email": "test@test.com",
        }
    )
)

print("\nNotification:")
print(
    send_booking_notification.invoke(
        {
            "email": "test@test.com",
            "date": "2026-07-20",
            "time": "10:00",
        }
    )
)