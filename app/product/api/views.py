from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from product.models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer
from .validators import validate_product_data, validate_order_data
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductFilter
import logging

logger = logging.getLogger(__name__)
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Categories retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': 201,
                'message': 'Category created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': 400,
            'message': 'Category creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Category retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class CategoryUpdateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def put(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': 200,
                'message': 'Category updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'status': 400,
            'message': 'Category update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({
            'success': True,
            'status': 204,
            'message': 'Category deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class ProductPagination(PageNumberPagination):
    page_size = 10

class ProductListView(APIView):
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['created_at']

    def get(self, request):
        queryset = Product.objects.all()

        # Apply filtering
        filter_backends = self.filter_backends
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        # Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(queryset, many=True)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Products retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
class ProductCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        
        errors = validate_product_data(request.data)
        if errors:
            return Response({
                'success': False,
                'status': 400,
                'message': 'Product creation failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': 201,
                'message': 'Product created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': 400,
            'message': 'Product creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Product retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class ProductUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        errors = validate_product_data(request.data)
        if errors:
            return Response({
                'success': False,
                'status': 400,
                'message': 'Product update failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': 200,
                'message': 'Product updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'status': 400,
            'message': 'Product update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None
    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({
            'success': True,
            'status': 204,
            'message': 'Product deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        product_data = {
            'products': serializer.data 
        }
        return Response({
            'success': True,
            'status': 200,
            'message': 'Orders retrieved successfully',
            'data': product_data
        }, status=status.HTTP_200_OK)

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'success': True,
                'status': 201,
                'message': 'Order created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': 400,
            'message': 'Order creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class OrderUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk, user=self.request.user)
        except Order.DoesNotExist:
            return None

    def put(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': 200,
                'message': 'Order updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'status': 400,
            'message': 'Order update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Order.objects.get(pk=pk, user=user)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk, request.user)
        if not order:
            return Response({
                'success': False,
                'status': 404,
                'message': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Order retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
