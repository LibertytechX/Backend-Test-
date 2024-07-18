from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework_simplejwt.tokens import AccessToken

from core.exceptions import raise_serializer_error_msg
from core.models import ProductCategory, Product, Order
from core.paginations import CustomPagination
from core.serializers import SignUpSerializerIn, LoginSerializerIn, UserSerializerOut, ProductCategorySerializerOut, \
    ProductSerializerIn, ProductSerializerOut, OrderPlacementSerializerIn, OrderSerializerOut


class SignUpAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = SignUpSerializerIn(data=request.data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        response = serializer.save()
        return Response({"detail": response})


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializerIn(data=request.data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        user = serializer.save()
        return Response({
            "detail": "Login Successful", "data": UserSerializerOut(user).data,
            "access_token": f"{AccessToken.for_user(user)}"
        })


class ProductCategoryListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    serializer_class = ProductCategorySerializerOut
    queryset = ProductCategory.objects.all().order_by("-created_on")


class ProductCreateUpdateDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ProductSerializerIn(data=request.data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        response = serializer.save()
        return Response({"detail": "Product created successfully", "data": response}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializerIn(data=request.data, instance=product)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        response = serializer.save()
        return Response({"detail": "Product updated successfully", "data": response})

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response({"detail": "Product deleted"})


class ProductListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = ProductSerializerOut
    queryset = Product.objects.all().order_by("-created_on")
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class OrderPlacementAPIView(APIView, CustomPagination):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderPlacementSerializerIn(data=request.data, context={"request": request})
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        response = serializer.save()
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request):
        data = Order.objects.filter(user=request.user).order_by("-created_on")
        queryset = self.paginate_queryset(data, request)
        serializer = OrderSerializerOut(queryset, many=True).data
        response = self.get_paginated_response(serializer).data
        return Response(response)









