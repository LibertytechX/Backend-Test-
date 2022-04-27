"""Manage admin page for main app."""

from django.contrib import admin
from .models import User

admin.site.register(User)

# Register your models here.
