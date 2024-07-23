from rest_framework import serializers
from .models import Category, Product, CartItem, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'price', 'stock_qty')

    
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category_name', 'in_stock', 'stock_qty', 'created_at']


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class OrderItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = "product.name")
    product_price = serializers.CharField(source = "product.price")
    class Meta:
        model= CartItem
        fields = ['id', 'product_name', 'product_price', 'quantity', 'is_ordered']

class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='user.name')
    items = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'items', 'created_at']

    def get_items(self, obj:Order):
        return OrderItemsSerializer(obj.orderitems.all(), many=True).data
