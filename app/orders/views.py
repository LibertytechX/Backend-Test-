from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from utils.mixins import SuccessResponseMixin

from .serializers import OrderSerializer


class OrderCreateView(SuccessResponseMixin, generics.CreateAPIView):
    serializer_class = OrderSerializer


class OrderHistoryView(SuccessResponseMixin, generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
