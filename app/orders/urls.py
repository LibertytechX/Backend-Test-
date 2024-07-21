from django.urls import path
from .views import OrderCreateView, OrderListView

urlpatterns = [
    path('order/', OrderCreateView.as_view(), name='order-create'),
    path('orders/history/', OrderListView.as_view(), name='order-history'),
]
