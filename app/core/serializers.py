from rest_framework import serializers
from .models import User, Category, Product, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'cover']

class ProductSerializer(serializers.ModelSerializer):
    categoryId = serializers.IntegerField(write_only=True, source='category.id')
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'price', 'categoryId', 'category', 'id']

    def create(self, validated_data):
        category_id = validated_data.pop('category')['id']
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product

    def update(self, instance, validated_data):
        if "category" in validated_data:
            cat = validated_data.pop('category')
            if cat and cat["id"]:
                category_id = cat['id']
                category = Category.objects.get(id=category_id)
                instance.category = category   
        if instance.name:
            instance.name = validated_data.get('name', instance.name)
        if instance.price:
            instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

class OrderItemSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['productId', 'product', 'quantity', 'price']

    def create(self, validated_data):
        product_id = validated_data.pop('productId')
        product = Product.objects.get(id=product_id)
        validated_data['product'] = product
        validated_data['price'] = validated_data['quantity'] * product.price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        product_id = validated_data.get('productId', instance.product.id)
        if product_id != instance.product.id:
            product = Product.objects.get(id=product_id)
            instance.product = product
            instance.price = validated_data.get('quantity', instance.quantity) * product.price
        else:
            instance.price = validated_data.get('quantity', instance.quantity) * instance.product.price
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            item_data['order'] = order
            OrderItemSerializer().create(item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance = super().update(instance, validated_data)

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                item_data['order'] = instance
                OrderItemSerializer().create(item_data)
        return instance
