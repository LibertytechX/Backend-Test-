from rest_framework import routers
from django.urls import path, include
from .views import ProductViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r"products", ProductViewSet, basename="products")


urlpatterns = [
    path("", include(router.urls)),
]
