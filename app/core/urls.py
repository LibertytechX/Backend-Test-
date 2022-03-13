from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register-user'),
    path('get_all_coins/', views.ListCoinsAPIView.as_view(), name='coin-list'),
    path('add_favourite/', views.AddFavoriteCoinsAPIView.as_view(), name='add_favourite'),
    path('view_favourites/', views.UserFavoriteCoinsListView.as_view(), name='view_favourites'),
]