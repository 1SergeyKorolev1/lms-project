from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import PaymentListAPIView, PaymentCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
]
