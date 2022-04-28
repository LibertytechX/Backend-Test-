from django.urls import path, include
from .views import UserClass, CoinClass, add_favourite, view_favourite


urlpatterns = [
    #path('viewsets/', include(router.urls)),
      path('api/user', UserClass.as_view(), name = 'userauth'),
       path('api/coins', CoinClass.as_view(), name = 'usercoins'),
       path('api/addFavorite',add_favourite, name = 'add-favorite'),
       path('api/getFavorites', view_favourite, name = 'get-favorites'),

]