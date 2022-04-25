from django.urls import path
from . import views 

urlpatterns = [
    path('view-favourites/<str:name>', views.view_favourites, name='view_favourties'),
    path('add/<str:name>', views.add_favourite, name='add-favourites'),
]