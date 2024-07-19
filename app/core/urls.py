from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import RegisterView, UserView, LoginView, CategoryListView, GetCategoryView, ListProductView, GetProductView, OrderListCreateView, OrderDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user'),
    path('categories/', CategoryListView.as_view(), name="categories"),
    path('categories/<int:pk>', GetCategoryView.as_view(), name="category"),
    path('products/', ListProductView.as_view(), name="products"),
    path('products/<int:pk>', GetProductView.as_view(), name="product"),
    path('orders/', OrderListCreateView.as_view(), name="orders"),
    path('orders/<int:pk>', OrderDetailView.as_view(), name="order"),
]
