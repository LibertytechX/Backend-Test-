from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import LargeResultsSetPagination


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    """This viewsets handles an authenticated user's product CRUD operations
    """
    queryset = Product.objects.all().order_by('-date_added')
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'price', 'category', 'date_added']
    search_fields = ['name', 'price', 'category__name', 'date_added']
    ordering_fields = ['price', 'category__name', 'date_added']
    pagination_class = LargeResultsSetPagination


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """This viewsets handles Product Category actions.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    ]
