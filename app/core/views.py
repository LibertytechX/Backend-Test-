from rest_framework.response import Response
from rest_framework import viewsets, permissions, decorators, response, filters, generics, status
from shop.permissions import IsOwnerOrAdmin
from shop.serializers import OrderSerializer
from .serializers import LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [
                permissions.IsAuthenticated, IsOwnerOrAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    @decorators.action(detail=False, methods=["GET"], url_path='order-history')
    def user_order_history(self, request):
        user = request.user

        histories = user.get_user_order_history()
        page = self.paginate_queryset(histories)

        if page is not None:
            serializer = OrderSerializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = OrderSerializer(
            histories, many=True, context={'request': request})
        return response.Response(serializer.data)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
