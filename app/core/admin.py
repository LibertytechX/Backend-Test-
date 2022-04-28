"""Manage admin page for main app."""

from django.contrib import admin
from .models import Favourite, User, AllCoins

admin.site.register(User)
admin.site.register(AllCoins)
admin.site.register(Favourite)

# Register your models here.
