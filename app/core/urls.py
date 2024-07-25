from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet
from .views import OrderViewSet, OrderHistoryAPIView,ProductListView, OrderProductListView






router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('orders/', OrderProductListView.as_view(), name='order-product-list'),
]

urlpatterns += [
    path('order-history/', OrderHistoryAPIView.as_view(), name='order-history'),
]




