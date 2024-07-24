from django.shortcuts import render
from products_App.models import Category, Products
from rest_framework import status
from rest_framework.views import APIView
from products_App.serializers import CartegorySerializers,ProductSerializers
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from products_App.pagination import CustomPagination
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CartegorySerializers
"""
class productCreateRetreiveAll(APIView):
    
    def post (self, request):
        serializer_class = ProductSerializers(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(data=serializer_class.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        user = Products.objects.all()
        serializer_class = ProductSerializers(user, many = True)
        pagination_class = CustomPagination
        return Response(data=serializer_class.data, status= status.HTTP_200_OK)
    
class ProductDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except:
            raise Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk, format = None):
        product = self.get_object(pk)
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        products = self.get_object(pk)
        serializer = ProductSerializers(products, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        
"""

class ProductSearch(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['Product_Name', 'Price']
    
class CatergoryCreateRetreiveAll(APIView):
    """Create and get all products

    Args:
        APIView (_type_): _description_
    """
    def post (self, request):
        serializer = CartegorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CartegorySerializers(categories, many = True)
        return Response(data=serializer.data, status= status.HTTP_200_OK)
    
class CatergoryDetail(APIView):
    """Retrieve, update or delete a Catergory from the database

    Args:
        APIView (_type_): _description_
    """
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except:
            raise Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk, format = None):
        product_cart = self.get_object(pk)
        serializer = ProductSerializers(product_cart)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        product_cart = self.get_object(pk)
        serializer = CartegorySerializers(product_cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product_cart = self.get_object(pk)
        product_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

