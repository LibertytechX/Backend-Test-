from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from products.models import Product, Category


class ProductSerializer(ModelSerializer):
    self_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "discount_price",
            "available_quantity",
            "self_url",
        )

    def get_self_url(self, obj):
        request = self.context.get("request")
        base_url = request.build_absolute_uri("/")[:-1]
        return f"{base_url}/products/{obj.pk}/"


class CreateProductSerializer(ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "discount_price",
            "available_quantity",
            "category",
        )
