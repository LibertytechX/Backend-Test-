from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import OwnerPermission
from .models import Order
from .serializers import OrderSerializer


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    """This viewsets handles an authenticated user's product CRUD operations
    """
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        OwnerPermission,
    ]

    def get_queryset(self):
        """ Filter orders by authenticated user. """
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def history(self, request):
        """ Returns history of ordered items. """

        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders,
                                     many=True,
                                     context={'request': request})
        return Response(serializer.data)
