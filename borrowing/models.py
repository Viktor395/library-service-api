from django.conf import settings
from django.db import models
from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )

    def __str__(self):
        return f"{self.user.email} borrowed {self.book.title} on {self.borrow_date}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        is_returning = False
        if not is_new:
            old_instance = Borrowing.objects.get(pk=self.pk)
            if old_instance.actual_return_date is None and self.actual_return_date is not None:
                is_returning = True

        super().save(*args, **kwargs)
        
        from borrowing.notification_helper import send_telegram_message

        if is_new:
            message = (
                f"🎉 <b>New Borrowing Created!</b>\n\n"
                f"👤 <b>User:</b> {self.user.email}\n"
                f"📚 <b>Book:</b> {self.book.title}\n"
                f"📅 <b>Borrow Date:</b> {self.borrow_date}\n"
                f"⏳ <b>Expected Return:</b> {self.expected_return_date}"
            )
            send_telegram_message(message)
            
        elif is_returning:
            message = (
                f"✅ <b>Book Returned Successfully!</b>\n\n"
                f"👤 <b>User:</b> {self.user.email}\n"
                f"📚 <b>Book:</b> {self.book.title}\n"
                f"📅 <b>Returned On:</b> {self.actual_return_date}\n"
                f"stocked back to inventory ✨"
            )
            send_telegram_message(message)
