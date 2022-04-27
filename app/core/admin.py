"""Manage admin page for main app."""

from django.contrib import admin
from .models import User, AllCoins

admin.site.register(User)
admin.site.register(AllCoins)

# Register your models here.
