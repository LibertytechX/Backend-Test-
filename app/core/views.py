from django.contrib.auth import login
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset handles User CRUD operations including login and register endpoints.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """ Login a user
            Returns JWT with access token expiring in 15 minutes
        """
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            # Email not found or password mismatch
            return Response(
                {
                    'status': 400,
                    'message': 'Email or password is incorrect'
                }, 400)

        if not user.is_active:
            return Response({
                'status': 400,
                'message': 'Inactive account'
            }, 400)

        # Login user and assign JWT

        login(request, user=user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """ Registers a user """
        return super().create(request)
