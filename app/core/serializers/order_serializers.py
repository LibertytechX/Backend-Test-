from rest_framework import serializers
from core.models import Product, Order, OrderProduct
from .product_serializers import ProductOrderSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, source='orderproduct_set')

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'date']


class OrderProductDetailSerializer(serializers.ModelSerializer):
    product = ProductOrderSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderProductDetailSerializer(
        many=True, source='orderproduct_set')

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'date']
