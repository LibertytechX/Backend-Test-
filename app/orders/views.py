from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from utils.mixins import SuccessResponseMixin

from .serializers import OrderSerializer


class OrderCreateView(SuccessResponseMixin, generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
