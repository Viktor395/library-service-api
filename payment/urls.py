from django.urls import path
from payment.views import payment_success, payment_cancel

urlpatterns = [
    path("success/", payment_success, name="payment-success"),
    path("cancel/", payment_cancel, name="payment-cancel"),
]

app_name = "payment"
