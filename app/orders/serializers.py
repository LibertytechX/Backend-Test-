from rest_framework import serializers
from .models import Order
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'quantity', 'date']
        read_only_fields = ['user', 'date']

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        order.products.set(products)
        return order
