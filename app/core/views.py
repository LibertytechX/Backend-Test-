from .models import User
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework import status
from .permissions import IsOwnerOrReadOnly, IsOwner


class CreateUser(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Created user successfully',
            'username': response.data['username'],
            'status': 200,
        })


class UserListAPIView(ListAPIView):
    """
    get:
        Returns list of all exisiting users
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
