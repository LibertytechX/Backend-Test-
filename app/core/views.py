from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
from utils.responses import success_response


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        data = {
            **serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

        return success_response(data, status_code=status.HTTP_201_CREATED)
