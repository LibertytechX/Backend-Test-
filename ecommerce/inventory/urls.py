from django.urls import path, include
from .views import RegisterView, LoginView, ProductViewSet, CategoryViewSet, OrderCreateView, OrderHistoryView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/history/', OrderHistoryView.as_view(), name='order-history'),

]