from django.shortcuts import render
from users.serializers import CreateUserSerializer, LoginSerializer
from utils.response import service_response
from utils.exceptions import handle_internal_server_exception
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from typing import Any

# Create your views here.


User = get_user_model()


class CreateUserAPIView(APIView):
    """Create a new user"""

    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        """Register a new user post handler"""
        try:
            serializer: CreateUserSerializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                #    save serializer
                serializer.save()
                return service_response(
                    status="success",
                    message="Registration Successful",
                    status_code=201,
                )
            return service_response(
                status="error", message=serializer.errors, status_code=400
            )
        except Exception:
            return handle_internal_server_exception()


class RootPage(APIView):
    def get(self, request, format=None):
        return service_response(
            status="success", message="Great, Welcome all good!", status_code=200
        )


class LoginUserAPIView(APIView):
    """Generates user access token and refresh token"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """Login user post handler"""
        try:
            serializer: LoginSerializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # get the user from the serializer validated data
                user: Any = serializer.validated_data.get("user")
                # get the token
                tokens: Any = RefreshToken.for_user(user)
                access_token: str = str(tokens.access_token)
                refresh_token: str = str(tokens)
                token_data: dict = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": tokens.access_token.lifetime.total_seconds(),
                }
                return service_response(
                    status="success",
                    data=token_data,
                    message="Login Successful",
                    status_code=200,
                )
            return service_response(
                status="error", message=serializer.errors["error"][0], status_code=400
            )

        except Exception:
            return handle_internal_server_exception()
