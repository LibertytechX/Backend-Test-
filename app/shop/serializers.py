from rest_framework import serializers

from .models import Product, Category, Order, OrderItem


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Product
        fields = ['url', 'id', 'category', 'name', 'description',
                  'price', 'stock', 'is_available']
        read_only_fields = ['is_available']


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    products = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='product-detail')

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'products']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'is_checked_out',
                  'created_at', 'updated_at', 'order_items']
