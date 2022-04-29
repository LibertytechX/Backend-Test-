"""Manage admin page for main app."""

from re import U
from django.contrib import admin

# Register your models here.
from core.models import User, FavCoin

class UserAdmin(admin.ModelAdmin):
    pass

class MyFavAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(FavCoin, MyFavAdmin)