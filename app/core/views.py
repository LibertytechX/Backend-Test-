from rest_framework import generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import UserSerializer, UserLoginSerializer, MyTokenObtainPairSerializer
from .models import Product, Category, Order, OrderProduct
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderProductSerializer
from rest_framework.permissions import IsAuthenticated

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    
    
    


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderHistoryAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


    
    
    
class ProductPagination(PageNumberPagination):
    page_size = 10  # Number of products per page

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)  # Fields to search in

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    
    
    
class OrderProductListView(generics.ListAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)  
        return queryset
    
