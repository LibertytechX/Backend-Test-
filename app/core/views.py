from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .serializers import UserRegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'user': serializer.data,
            'message': 'User created successfully.'
        }, status=status.HTTP_201_CREATED)