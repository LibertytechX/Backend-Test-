from .serializers import UserSerializer
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.
class UserRegistrationEndpoint(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


