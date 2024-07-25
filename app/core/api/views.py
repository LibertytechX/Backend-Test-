from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import *
from .validators import validate_user_data
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
class UserCreateView(APIView):
    def post(self, request):
        data = request.data
        errors = validate_user_data(data)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'success': True,
                'status': 200,
                'message': 'User Created Successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'success':True,'status':200,'message':'User logged out successfully'},status =status.HTTP_200_OK)
        except Exception as e:
            return Response({'success':False,'status':400,'message': str(e) },status =status.HTTP_400_BAD_REQUEST)