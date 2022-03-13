"""app URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # CREATE NEW USER VIA API
    path('register/', views.CreateUser.as_view()),

    # GET ALL COINS
    path('getcoins/', views.GetCoins.as_view()),

    # ADD FAVOURITES VIA API
    path('addfavourite/', views.AddFavourite.as_view()),

    # VIEW FAVOURITES FOR SPECIFIC USER
    path('viewfavourites/', views.ViewFavourites.as_view()),

    # CREATE COINS VIA API (MANAGEMENT COMMANDS) TO SEED DATABASE
    path('loaddb/', views.LoadDB.as_view()),

]
