# Django Iports
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
#  USER
##########################
class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Creates, Updates and Retrieves - User Accounts
    """
    # parser_classes = (MultiPartParser, FormParser)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    queryset = User.objects.all().order_by('-id')
    serializers = {
        'default': UserSerializer,
    }
    
    permission_classes = [
        IsJWTValidated
    ]
    
    def get_queryset(self):                                      
        return super().get_queryset()
    
    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
    
    def list(self, request):
        queryset = self.get_queryset()
        queryset = self.queryset.filter(
            Q(name__icontains = request.query_params.get('search') if request.query_params.get('search') else '') |
            Q(email__icontains = request.query_params.get('search') if request.query_params.get('search') else ''),
            is_active = True
        ).values()
        try:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                paginated_response.data['message'] = "Users retrived successfully"
                return paginated_response

        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            if instance.is_active:
                serializer = self.get_serializer(instance)
                return Response({"message":"User retrived successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            
            else:
                return Response({'message': 'User has been dactivated'}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            if instance.is_active:
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User has been dactivated'}, status=status.HTTP_403_FORBIDDEN)
                    
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
        
    
    def destroy(self, request, *args, **Kwargs):
        """
        Delete user
        """
        try:
            instance = self.get_object()
        except:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            instance = self.get_object()
            instance.is_active = False
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message":"User deleted successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
