from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_user, name='register'),
    path("get-all-coins", views.get_all_coins, name="get-all-coins"),
    path('view-favourites/<str:name>', views.view_favourites, name='view_favourties'),
    path('add/<str:name>', views.add_favourite, name='add-favourites'),
]