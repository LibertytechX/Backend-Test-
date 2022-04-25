from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home_view, name="home"),
    path("register", views.register_user, name='register'),
    path("get-all-coins", views.get_all_coins, name="get-all-coins")
]
