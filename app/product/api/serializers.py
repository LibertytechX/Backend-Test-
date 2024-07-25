from rest_framework import serializers
from product.models import Category, Product, Order, OrderProduct

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'stock', 'sku', 'created_at', 'updated_at']
        read_only_fields = ['id', 'category_name', 'created_at', 'updated_at']

    def get_category_name(self, obj):
        return obj.category.name

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_id', 'quantity', 'price']
        read_only_fields = ['id', 'price']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='order_products', many=True, write_only=True)
    order_products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'date', 'status', 'total_amount', 'shipping_address', 'billing_address', 'products', 'order_products']
        read_only_fields = ['user', 'date', 'total_amount', 'order_products']

    def create(self, validated_data):
        products_data = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        for item in products_data:
            OrderProduct.objects.create(order=order, **item)
        return order

    def update(self, instance, validated_data):
        products_data = validated_data.pop('order_products')
        instance.status = validated_data.get('status', instance.status)
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.billing_address = validated_data.get('billing_address', instance.billing_address)
        instance.save()

        # Clear existing order products and create new ones
        instance.order_products.all().delete()
        for item in products_data:
            OrderProduct.objects.create(order=instance, **item)
        return instance