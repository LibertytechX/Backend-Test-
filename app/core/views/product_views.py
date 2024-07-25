# views.py
from rest_framework import viewsets
from rest_framework import exceptions as rest_exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


from core.models import Product, Category
from core.serializers.product_serializers import CategorySerializer, ProductCreateSerializer, ProductSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ProductPagination(PageNumberPagination):
    page_size = 5


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        data = request.data
        serializer = ProductCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    pagination_class = ProductPagination
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price']


class ProductGetDetailView(generics.RetrieveAPIView,):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, pk):
        try:
            inventory = Product.objects.get(pk=pk)
            serializer = ProductSerializer(inventory, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            raise rest_exceptions.ParseError('Product not found')


class ProductUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)

            data = request.data

            data_obj = {
                "name": data.get("name", product.name),
                "price": data.get("price", product.price),
                "quantity": data.get("quantity", product.quantity),
                "description": data.get("description", product.description),
                "category": data.get("category", product.category),
            }

            serializer = ProductCreateSerializer(
                product, data=data_obj, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Product.DoesNotExist:
            raise rest_exceptions.NotFound(detail="Product not found.")
        except Exception as e:
            raise rest_exceptions.ParseError(f"An error occurred: {str(e)}")

    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            message = {
                "message": "Product deleted successfully"
            }
            return Response(message, status=status.HTTP_200_OK)
        except:
            raise rest_exceptions.ParseError('Product not found')
