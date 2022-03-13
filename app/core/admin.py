"""Manage admin page for main app."""

from django.contrib import admin
from .models import User, FavouriteCoin

class UserAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = (
        'id',
        'email',
        'username',
        'favorite_coins'
    )

    def favorite_coins(self, user):
        coin_names = [str(coin) for coin in user.favourite_coins.all()]
        if len(coin_names) == 0:
            return "-"
        return str(coin_names)

admin.site.register(User, UserAdmin)