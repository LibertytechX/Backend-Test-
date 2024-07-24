from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()


routers.register("order", views.OrderView, basename='order')
routers.register("cart", views.CartItemView, basename='cart')

urlpatterns = [
    path("products/", views.ProductAPIView.as_view(), name="create_product"),
    path("products/<int:pk>/", views.ProductAPIView.as_view(), name="product_detail"),
    # path("cart", views.CartView.as_view(), name='cart'),
    # path("cartitem/<int:pk>/", views.CartItemView.as_view(), name='cartitem'),
    path("verify-order/<int:pk>/", views.VerifyOrder.as_view(), name='verify'),
]

urlpatterns += routers.urls
