from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(
    "products", ProductViewSet, basename='products'
)
router.register(
    "category", CategoryViewSet, basename="category"
)
router.register(
    "order", OrderViewSet, basename="order"
)

urlpatterns =[

]+router.urls