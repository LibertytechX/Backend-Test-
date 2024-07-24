from django.urls import path, include
from products_App.views import ProductViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'products', ProductViewSet)
urlpatterns = [
    path('', include(router.urls)),
    #path('CreateProduct/', productCreateRetreiveAll.as_view(), name='CreateProduct'),
    #path('products/', productCreateRetreiveAll.as_view(), name='products'),
    #path('DeleteProduct/', ProductDetail.as_view(), name='DeleteProduct'),
    #path('UpdateProduct/', ProductDetail.as_view(), name='UpdateProduct'),
]