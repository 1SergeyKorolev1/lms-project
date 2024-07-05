from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    """создание платежа"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_price(payment.payment_amount, product_id)
        session_id, payment_url = create_stripe_session(price)
        payment.session_id = session_id
        payment.url = payment_url
        payment.save()


class PaymentListAPIView(generics.ListAPIView):
    """
    отображение списка платежей, с фильтрацией и сортировкой
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    if queryset.count()!= 0:
        filter_backends = [DjangoFilterBackend, OrderingFilter]
        filterset_fields = (
            "paid_course",
            "paid_lesson",
            "payment_method",
        )
        ordering_fields = ("date_payment",)
