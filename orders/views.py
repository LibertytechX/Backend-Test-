from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from orders.serializers import OrderListSerializer, OrderSerializer
from utils.response import service_response
from utils.exceptions import handle_internal_server_exception
from .models import Order
from rest_framework import serializers
import re


class PlaceOrderAPIView(APIView):
    """Place order api view"""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        """Place order post handler"""
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return service_response(
                    status="success",
                    message="Order placed successfully",
                    status_code=201,
                )
            return service_response(
                status="error",
                message=serializer.errors,
                status_code=400,
            )
        except serializers.ValidationError as e:
            match = re.search(r"Product (\d+) not found", str(e.detail))
            message = str(match.group())
            return service_response(
                status="error",
                message=message,
                status_code=400,
            )
        except Exception:
            return handle_internal_server_exception()


class OrderListAPIView(APIView):
    """List all order history for authenticated user"""

    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get(self, request, *args, **kwargs):
        """List all orders get handler"""
        try:
            user = request.user
            orders = Order.objects.filter(user=user)
            serializer = self.serializer_class(orders, many=True)
            return service_response(
                status="success",
                data=serializer.data,
                status_code=200,
            )
        except Exception:
            return handle_internal_server_exception()
