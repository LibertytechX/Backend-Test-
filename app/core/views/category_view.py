# Django Iports
from django.db.models import Q


# DRF Imports
from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

# Core Imports
from core.permissions import IsJWTValidated
from core.models import *
from core.serializers import *


##########################
#  CATEGORY
##########################
class CategoryViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('id')
    serializers = {
        'default': CategorySerializer,
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
        Create category
        """
        queryset = self.get_queryset()
        
        try:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                paginated_response.data['message'] = "Categories retrived successfully"
                return paginated_response
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request):
        """
        Create category
        """
        try:
            category = self.queryset.filter(name = request.data['name']).exists()
            if category:
                return Response({'message': 'Category already exists'}, status=status.HTTP_409_CONFLICT)
                
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({"message": "Category created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def retrieve(self, request, *args, **kwargs):
        """
        Get category
        """
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            serializer = self.get_serializer(instance)
            return Response({"message":"Category retrived successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def update(self, request, *args, **kwargs):
        """
        Update category
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Category updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def destroy(self, request, *args, **Kwargs):
        """
        Delete category
        """
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message":"Category deleted successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
