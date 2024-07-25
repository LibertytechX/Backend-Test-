from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('product-list/', ProductListApiView.as_view()),
    path('detail/<str:name>/<slug:slug>/', ProductDetailApiView.as_view()),
    path('cart/add/<int:product_id>/', CartAddView.as_view()),
    path('cart/remove/<int:product_id>/', CartRemoveView.as_view()),
    path('cart/details/', CartDetailView.as_view()),
    path('cart/clear/', CartClearView.as_view()),
]
