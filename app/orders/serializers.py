from django.db import transaction
from rest_framework import serializers

from core.serializers import UserSerializer
from products.models import Product

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "total_amount", "items", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context.get('request').user
        with transaction.atomic():
            order = Order.objects.create(**validated_data, user=user)
            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)
            return order
