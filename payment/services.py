import stripe
from django.conf import settings
from django.urls import reverse
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_session(borrowing, request, payment_type="PAYMENT"):
    duration = (borrowing.expected_return_date - borrowing.borrow_date).days
    if duration <= 0:
        duration = 1

    total_price = duration * borrowing.book.daily_fee

    stripe_amount = int(total_price * 100)

    base_url = request.build_absolute_uri("/")[:-1]
    
    success_url = base_url + reverse("payment:payment-success") + "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = base_url + reverse("payment:payment-cancel")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Borrowing: {borrowing.book.title}",
                    "description": f"Rent for {duration} days",
                },
                "unit_amount": stripe_amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )

    payment = Payment.objects.create(
        status=Payment.StatusChoices.PENDING,
        type=payment_type,
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=total_price
    )

    return payment
