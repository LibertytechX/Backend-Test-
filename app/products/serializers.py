from django.urls import reverse
from rest_framework import serializers
from .models import ProductCategory, Product


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=ProductCategory.objects.all(), slug_field='name')
    links = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_links(self, obj):
        """ Implement HATEOAS protocol in API """
        return {
            'href': reverse('products-detail', kwargs={'pk': obj.id}),
            'rel': 'products',
            'type': 'GET'
        }
