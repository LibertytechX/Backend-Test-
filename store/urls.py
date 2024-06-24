from django.urls import path
from .views import place_order, order_history

urlpatterns = [
    path("orders/", place_order, name="place-order"),
    path("orders/history/", order_history, name="order-history"),
]
