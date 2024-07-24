from Order_App.views import OrderViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'categories', CategoryViewSet)
#router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/place_order/', OrderViewSet.as_view({'post': 'place_order'}), name='place_order'),
    path('orders/order_history/', OrderViewSet.as_view({'get': 'order_history'}), name='order_history'),
]