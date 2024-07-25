from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'is_deleted', 'category']
    search_fields = ['name']
   
    def destroy(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(Products.objects.all(),pk=pk)
        product.is_deleted = True
        product.save()

        return Response("Item has been archived", status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post','delete'], permission_classes=[IsAuthenticated])
    def hard_delete(self, request, pk=None):
        product = get_object_or_404(Products.objects.all(),pk=pk)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name','is_deleted']
    search_fields = ['name']

    def destroy(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(Category.objects.all(),pk=pk)
        product.is_deleted = True
        product.save()

        return Response("Item has been archived", status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post','delete'], permission_classes=[IsAuthenticated])
    def hard_delete(self, request, pk=None):
        product = get_object_or_404(Category.objects.all(),pk=pk)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderItemViewset(ModelViewSet):
    queryset = OrderedItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['products']
    search_fields = ['products']


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_completed', 'date']

    

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            order_total = sum(order.get_total_price for order in page)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        order_total = sum(order.get_total_price for order in queryset)

        response_data = {
            "data": serializer.data,
            "order_total": order_total
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(Order,pk=pk,user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

       
    
   
    
    

    