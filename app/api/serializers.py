from rest_framework import serializers
from ..shop.models import Product, Category
from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer

class ProductSerializer(serializers.ModelSerializer):
    """
    Product model serializer
    """
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ["category", "name", "slug", "image", "description", "price", "available", "created", "updated", "owner"]


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'password']


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'password']
