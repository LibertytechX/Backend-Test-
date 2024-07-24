from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status


from .models import *
from .serializers import *

class ProductViewSet(ViewSet):
    queryset = Products
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    # def get_permissions(self):
        
    #     if self.action == "create" or self.action == "destroy":
    #        self.permission_classes = [IsAdminUser]
    #     return [permission() for permission in self.permission_classes]
    
    def list(self, request):
        queryset = self.queryset.objects.all()
        serializer = self.serializer_class(queryset, many=True)        
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors)
    

class CategoryViewSet(ViewSet):

    queryset = Category
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = self.queryset.objects.all()
        serializer = self.serializer_class(queryset, many=True)        
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors)
    

class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def list(self, request):
        order = Order.objects.filter(user=request.user, is_completed=False)
        serializer = self.serializer_class(order, many=True)
        
        order_total = 0
        for i in range(len(order)):
            order_total += order[i].get_total_price

        return Response({
            "data":serializer.data, "order_total":order_total
        })
    

    