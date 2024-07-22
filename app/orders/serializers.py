from django.urls import reverse
from rest_framework import serializers
from core.serializers import UserSerializer
from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_links(self, obj):
        """ Implement HATEOAS protocol in API """
        return {
            'href': reverse('orders-detail', kwargs={'pk': obj.id}),
            'rel': 'orders',
            'type': 'GET'
        }

    def create(self, validated_data):
        """ Handle creation of a new order """
        order_products = validated_data.pop("products")
        user = self.context.get(
            'request').user  # Owner of order is the current logged in user
        validated_data.update({'user': user})
        order = Order.objects.create(**validated_data)
        for order_product in order_products:
            order_product = OrderProduct.objects.create(**order_product)
            order.products.add(order_product)
        order.save()
        return order
