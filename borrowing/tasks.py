from datetime import date
from celery import shared_task
from borrowing.models import Borrowing
from borrowing.notification_helper import send_telegram_message

@shared_task
def check_overdue_borrowings():
    today = date.today()
    
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=today,
        actual_return_date__isnull=True
    )

    if not overdue_borrowings.exists():
        send_telegram_message("📉 No borrowings overdue today!")
        return

    message = "⚠️ <b>Overdue Borrowings List:</b>\n\n"
    
    for borrowing in overdue_borrowings:
        message += (
            f"👤 <b>User:</b> {borrowing.user.email}\n"
            f"📚 <b>Book:</b> {borrowing.book.title}\n"
            f"⏳ <b>Deadline was:</b> {borrowing.expected_return_date}\n"
            f"---------------------------\n"
        )
        
    send_telegram_message(message)
