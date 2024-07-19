from rest_framework import generics
from .models import User, Product, Category, OrderItem, Order
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, OrderItemSerializer, OrderSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from datetime import datetime
from .permissions import IsStaff
import logging
from django.utils import timezone

logging = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        data = {"email": request.data.get("email"), "password": request.data.get("password")}
        if request.data.get("is_staff"):
            data["is_staff"] = True
        if not data["email"] or not data["password"]:
            return Response({"message": "email and password is required", status: status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            return Response({"message": "user not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        
        if user.password != data["password"]:
            return Response({"message": "Incorrect password", "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            serialized = UserSerializer(user)
            User.objects.filter(email=data["email"]).update(last_login=timezone.now())
            return Response({"user":serialized.data, "token": { "access": str(access), "refresh": str(refresh)}}, status=status.HTTP_200_OK)
        except Exception as err:
            print(f"error occured: {err}")
            return Response({"message": "internal server error", "details": err}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated, IsStaff]
        return super().get_permissions()
    


class GetCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field="pk"
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsStaff]
        return super().get_permissions()
    

class ListProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated, IsStaff]
        return super().get_permissions()

        

class GetProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field="pk"
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsStaff]
        return super().get_permissions()
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BaseOrderView:
    """
    A base view to provide common queryset logic for Order views.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)


class OrderListCreateView(BaseOrderView, generics.ListCreateAPIView):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(BaseOrderView, generics.RetrieveUpdateDestroyAPIView):
    lookup_field="pk"