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
#  ORDER
##########################
class OrderViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all().order_by('-date_created')
    serializers = {
        'default': OrderSerializer,
        'create': CreateOrderSerializer,
        'update': UpdateOrderSerializer,
        'partial_update': UpdateOrderSerializer,
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
        Create order
        """
        queryset = self.get_queryset()
        queryset = self.queryset.filter(user_id = request.user.id)
        try:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                paginated_response.data['message'] = "Orders retrived successfully"
                return paginated_response
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def create(self, request):
        """
        Create order
        """        
        try:
            user = User.objects.filter(id = request.data['user'])[0]
            if user is None:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            if not user.is_active:
                return Response({'message': 'User has been deactivated'}, status=status.HTTP_403_FORBIDDEN)
            
            for product_id in request.data['products']:
                if not Product.objects.filter(id = product_id).exists():
                    return Response({'message': f'Product {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)
                    
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            serializer = OrderSerializer(Order.objects.get(id = serializer.data['id']))
            return Response({"message": "Order created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def retrieve(self, request, *args, **kwargs):
        """
        Get order
        """
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            serializer = self.get_serializer(instance)
            return Response({"message":"Order retrived successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def update(self, request, *args, **kwargs):
        """
        Update order
        """
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            if 'products' in dict(request.data).keys():
                for product_id in request.data['products']:
                    if not Product.objects.filter(id = product_id).exists():
                        return Response({'message': f'Product {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if 'user' in dict(request.data).keys():
                user = User.objects.filter(id = request.data['user'])[0]
                if user:
                    if not user.is_active:
                        return Response({'message': 'User has been deactivated'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            serializer = OrderSerializer(Order.objects.get(id = serializer.data['id']))
            return Response({"message": "Order updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **Kwargs):
        """
        Delete order
        """
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message":"Order deleted successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)