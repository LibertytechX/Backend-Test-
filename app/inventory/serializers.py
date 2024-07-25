from django.shortcuts import get_object_or_404
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
    id = serializers.IntegerField(required=False)
    class Meta:
        model = OrderedItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
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
    
    def update(self, instance,validated_data):
        print(validated_data)
        items = validated_data.pop("items")

        instance.is_completed = validated_data.get("is_completed", instance.is_completed)
        instance.save()
        all_item_ids = [item.id for item in instance.items.all()]
        print(all_item_ids)
        for item in items:
            print(item)
            item_id = item.get("id",None)
            if item_id and item_id in all_item_ids:
                order_item = get_object_or_404(OrderedItem, id=item_id)
                order_item.product = item.get("product", order_item.quantity)
                order_item.quantity = item.get("quantity", order_item.quantity)

                order_item.save()

            else:
                order_item = OrderedItem.objects.create(quantity=item['quantity'], product=item['product'])
                instance.items.add(order_item)

                instance.save()

            return instance