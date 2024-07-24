from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderedItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, )
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset = User
    )

    class Meta:
        model = Order
        fields = "__all__"

    
    def create(self, validated_data):
        items = validated_data.pop("items")

        order = Order.objects.create(**validated_data)

        for item in items:
            order_item = OrderedItem.objects.create(**item)
            order.items.add(order_item)

            order.save()

        return order