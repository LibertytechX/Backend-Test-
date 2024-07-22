"""Manage admin page for main app."""

from django.contrib import admin
from .models import User

# Register your models here
admin.site.register(User)
