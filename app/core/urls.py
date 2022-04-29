from audioop import add
from django.urls import path
from core.views import register, get_all_coins, add_favorite, view_favorites


urlpatterns = [
    path('register/', register, name="register"),
    path('get_all_coins/', get_all_coins, name="get_all_coins"),
    path('add_favourite/', add_favorite, name="add_favourite"),
    path('view_favourites/', view_favorites, name='view_favorites')
]