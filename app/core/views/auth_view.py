import jwt
from datetime import datetime, timedelta

# Django Iports
from django.contrib.auth import login, logout, authenticate

# DRF Imports
from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters

# Core Imports
from app.settings import SECRET_KEY
from core.models import *
from core.serializers import *



##########################
#  AUTH
##########################
class AuthViewSet(viewsets.GenericViewSet):
    # parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()
    serializers = {
        'default': UserSerializer,
        'register': CreateUserSerializer,
        'login_view': LoginUserSerializer,
        'logout_view': LogoutUserSerializer,
        'reset_password': ResetPasswordSerializer,
        'request_password_reset': RequestPasswordResetSerializer,
    }
    
        
    def get_queryset(self):                                      
        return super().get_queryset()
    
    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
    
    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def session(self, instance):
        """
        Fetch user in session
        """
        try:
            return Response({'message': 'User details fetched successfully', 'data': UserSerializer(self.request.user, context={'request': self.request}).data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Wrong auth token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=False, methods=['post'], url_path='register', url_name='register')
    def register(self, request):
        """
        User registeration
        """
        try:
            user = self.queryset.filter(email = request.data['email'].lower()).exists()
            if user:
                return Response({'message': 'Email already exists'}, status=status.HTTP_409_CONFLICT)
                
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    @action(detail=False, methods = ['post'], url_path='login', url_name='login')
    def login_view(self, request):
        """
        User login 
        """
        try:
            user = self.queryset.get(email = request.data['email'].lower())
            if user:
                if  user.is_active:
                    user = authenticate(email=request.data['email'].lower(), password=request.data['password'])
                    if user:    
                        serializer = self.get_serializer(user, data=request.data)
                        serializer.is_valid(raise_exception=True)
                        login(self.request, user)
                        return Response({'mesesage':'Logged in successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'User has been dactivated'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': f'Something went wrong {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    @action(detail=False, methods = ['post'], url_path='request-password-reset', url_name='request-password-reset')
    def request_password_reset(self, request):
        """
        Send password reset link 
        """
        try:
            user = self.queryset.get(email = request.data['email'].lower())
            if user:
                if  user.is_active:
                    # Append token to FE url as a query parameter
                    reset_token = jwt.encode(
                        {'id': user.id, 'exp': datetime.now() + timedelta(minutes=10)},
                        SECRET_KEY, algorithm="HS256"
                    )
                    
                    # Token is being returned for the purpose of testing the endpoint 
                    return Response({'message': 'Reset mail sent', 'data': reset_token}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'User has been dactivated'}, status=status.HTTP_403_FORBIDDEN)
                
            else:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    @action(detail=False, methods = ['post'], url_path='reset-password', url_name='reset-password')
    def reset_password(self, request):
        """
        Password reset
        """        
        try:
            payload: dict = jwt.decode(str(request.data['token']), SECRET_KEY, algorithms=["HS256"])
        except:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user: User = self.queryset.get(id = payload['id'])    
            if user:
                if  user.is_active:
                    user.set_password(request.data['password'])
                    user.save()
                    return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
                
                else:
                    return Response({'message': 'User has been dactivated'}, status=status.HTTP_403_FORBIDDEN)
                
            else:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    @action(detail=False, methods = ['post'], url_path='logout', url_name='logout')
    def logout_view(self, request):
        """
        Remove user from session
        """
        try:
            RefreshToken(str(request.data['refresh'])).blacklist()           
        except:
            return Response({'messgae': 'Token is invalid or already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:               
            logout(request)             
            request.user = None              
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'messgae': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

