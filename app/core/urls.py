from django.urls import path
from .views import AddItemsToCart, PlaceOrder, CustomerOrderHistory

urlpatterns =[
    path('add-to-cart', AddItemsToCart.as_view(), name='add-items-to-cart'),
    path('place-order', PlaceOrder.as_view(), name='place-order'),
    path('order-history', CustomerOrderHistory.as_view(), name='orders')
]