from datetime import date
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingCreateSerializer
from payment.services import create_stripe_session


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_staff:
            queryset = queryset.filter(user=user)
        else:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user_id=user_id)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            is_active = is_active.lower() in ["true", "1"]
            queryset = queryset.filter(actual_return_date__isnull=is_active)

        return queryset

    def perform_create(self, serializer):
        with transaction.atomic():
            borrowing = serializer.save(user=self.request.user)

            try:
                payment = create_stripe_session(borrowing, self.request)
                stripe_url = payment.session_url
            except Exception as e:
                stripe_url = "Stripe Service Temporarily Unavailable"
                print(f"Stripe error: {e}")

            message = (
                f"📚 New Borrowing Created!\n"
                f"Ref No: {borrowing.id}\n"
                f"User: {borrowing.user.email}\n"
                f"Book: '{borrowing.book.title}'\n"
                f"Expected Return: {borrowing.expected_return_date}\n"
                f"💳 Pay Here: {stripe_url}"
            )
            
            print(f"[TELEGRAM NOTIFICATION]: {message}")

    @action(methods=["POST"], detail=True, url_path="return")
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            borrowing.actual_return_date = date.today()
            borrowing.book.inventory += 1
            borrowing.book.save()
            borrowing.save()

        return_message = f"✅ Book '{borrowing.book.title}' was returned!"

        return Response(BorrowingSerializer(borrowing).data, status=status.HTTP_200_OK)
