from rest_framework import viewsets

from utils.mixins import SuccessResponseMixin

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(SuccessResponseMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

