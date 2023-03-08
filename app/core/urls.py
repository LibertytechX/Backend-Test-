from django.urls import path
from .views import RegisterView, ListAndCreateCoinApiView, AddFavouriteView, GetMyFavouriteView, upload_data_view
from .utils import get_coin_data

urlpatterns = [
    path("register/", RegisterView.as_view(), name='Register'),
    path("coins/", ListAndCreateCoinApiView.as_view(), name="coins"),
    path("get-coins/", upload_data_view, name="get-coins"),
    path("favourite/", AddFavouriteView.as_view(), name="Favourite"),
    path("getfav/", GetMyFavouriteView.as_view(), name="getfav")
]