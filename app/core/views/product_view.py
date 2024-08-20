

# Django Iports
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.db.models import Q


# DRF Imports
from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

# Core Imports
from app.settings import SECRET_KEY
from core.permissions import IsJWTValidated
from core.models import *
from core.serializers import *


##########################
#  PRODUCT
##########################
class ProductViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializers = {
        'default': ProductSerializer,
    }
    
    permission_classes = [
        IsJWTValidated
    ]
    
    def get_queryset(self):                                      
        return super().get_queryset()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def list(self, request):
        """
        List products
        """
        queryset = self.get_queryset()
        queryset = self.queryset.filter(
            Q(name__icontains = request.query_params.get('search') if request.query_params.get('search') else '')
        ).values()
        try:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                paginated_response.data['message'] = "Products retrived successfully"
                return paginated_response
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def create(self, request):
        """
        Create product
        """        
        try:
            category = Category.objects.filter(id = request.data['category']).exists()
            if not category:
                return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
            
            product = self.queryset.filter(name = request.data['name']).exists()
            if product:
                return Response({'message': 'Product already exists'}, status=status.HTTP_409_CONFLICT)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({"message": "Product created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def retrieve(self, request, *args, **kwargs):
        """
        Get product
        """
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            serializer = self.get_serializer(instance)
            return Response({"message":"Product retrived successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, *args, **kwargs):
        """
        Update product
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            if 'category' in dict(request.data).keys():
                category = Category.objects.filter(id = request.data['category']).exists()
                if not category:
                    return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
        
    
    def destroy(self, request, *args, **Kwargs):
        """
        Delete product
        """
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message":"Product deleted successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

