# serializers.py
from rest_framework import serializers
from core.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'category']


class ProductOrderSerializer(serializers.ModelSerializer):
    category = serializers.CharField(read_only=True, source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']
