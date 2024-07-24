from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import * 

User = get_user_model()


class UserRegistrationView(APIView):
    queryset = User
    serializer_class = UserRegistrationSerializers

    def post(self, request):

        serializers = self.serializer_class(data=request.data)
        
        if serializers.is_valid():
            serializers.save()

            user = User.objects.get(email=serializers.data['email'])

            token = RefreshToken.for_user(user)

            return Response({
                "refresh":str(token),
                "access":str(token.access_token),
               

            }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    



class LoginView(APIView):
    pass