from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment


@api_view(["GET"])
def payment_success(request):
    session_id = request.query_params.get("session_id")

    if not session_id:
        return Response(
            {"error": "Missing session_id parameter"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        payment = Payment.objects.get(session_id=session_id)

        payment.status = "PAID"
        payment.save()

        return Response(
            {"message": f"Payment successful for session {session_id}!"},
            status=status.HTTP_200_OK,
        )

    except Payment.DoesNotExist:
        return Response(
            {"error": "Payment record not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
def payment_cancel(request):
    return Response(
        {"message": "Payment was canceled. You can pay later within 24 hours."},
        status=status.HTTP_400_BAD_REQUEST,
    )
