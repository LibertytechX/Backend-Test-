from rest_framework import viewsets, filters

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from app.utilis import ProductPagePagination

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer