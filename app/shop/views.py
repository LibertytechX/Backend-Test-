
from rest_framework import viewsets, pagination, filters, routers, generics, decorators, response, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse


from .models import Order, OrderItem, Product, Category
from .serializers import (
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
    CategorySerializer,
)

from .permissions import IsOwnerOrAdmin

# Create your views here.


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ExtraUtilityMixin:
    filter_backends = [filters.SearchFilter]
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        elif self.action in ["update", "partial_update", "destroy", "create"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class ProductViewSet(ExtraUtilityMixin, viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    search_fields = ["name", "category__name"]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            # superusers can perform CRUD operations on available and unavailable products
            return Product.objects.all()
        # normal users can only view products in stock
        return Product.available.all()


class CategoryViewSet(ExtraUtilityMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    search_fields = ["name"]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        return super().perform_create(serializer)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    @decorators.action(detail=True, methods=["POST"], url_path='check-outorder-history')
    def check_out(self, request, *args, **kwargs):
        order = self.get_object()

        if not order.is_checked_out:
            order.check_out_order()
            return response.Response(status=status.HTTP_200_OK)
        return response.Response({"detail": "Order is already checked out."}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)


router = routers.DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"orderitem", OrderItemViewSet, basename="orderitem")
router.register(r"order", OrderViewSet, basename="order")


class ApiRoot(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                'categories': reverse('category-list', request=request),
                "products": reverse("product-list", request=request),
                "order_items": reverse("orderitem-list", request=request),
                "orders": reverse("order-list", request=request),
            }
        )
