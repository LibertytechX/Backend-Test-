from django.urls import path
from .views import OrderListAPIView, PlaceOrderAPIView

urlpatterns = [
    path("orders/place", PlaceOrderAPIView.as_view(), name="place-order"),
    path("orders", OrderListAPIView.as_view(), name="order-history"),
]
