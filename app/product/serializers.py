from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
    def validate_name(self, value):
        value = value.lower().strip()
        
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category',"image"]