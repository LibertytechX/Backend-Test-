from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterUserView.as_view(), name='register-user'),
    path('getcoins/', views.ListCoinsAPIView.as_view(), name='coin-list'),
    path('addfavourite/', views.AddFavoriteCoinsAPIView.as_view(), name='add-favourite'),
    path('viewfavourites/', views.UserFavoriteCoinsListView.as_view(), name='view-favourites'),
]