from rest_framework import viewsets, permissions, generics, response, status
from rest_framework.views import APIView
from . import serializers, models


class ProductCategory(viewsets.ModelViewSet):
    serializer_class=serializers.CategorySerializer
    queryset = models.Category.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    

class ProductCrudEndpoints(viewsets.ModelViewSet):
    queryset= models.Product.objects.all()   

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.ProductSerializer      
        return serializers.ProductCreateSerializer
    


class AddItemsToCart(generics.CreateAPIView):
    serializer_class=serializers.CartCreateSerializer
    queryset = models.CartItem.objects.all()
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class PlaceOrder(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        """get cart item that has been select but not ordered yet"""
        items = models.CartItem.objects.filter(user=request.user, is_ordered=False)
        if items.exists():
            order = models.Order.objects.create(user=request.user)
            order.orderitems.add(*items)
            items.update(is_ordered=True)
            return response.Response({'message':'order place successfully'}, status=status.HTTP_200_OK)
        return response.Response({'message':'no product selected yet'}, status=status.HTTP_400_BAD_REQUEST)
    

class CustomerOrderHistory(generics.ListAPIView):
    serializer_class= serializers.OrderSerializer
    queryset = models.Order.objects.all()
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset= queryset.filter(user=self.request.user)
        return queryset