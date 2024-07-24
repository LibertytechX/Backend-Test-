from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('user/', views.CustomersView.as_view(), name='user')
]
