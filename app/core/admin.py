"""Manage admin page for main app."""

from django.contrib import admin
from .models import User, Product, Category, Order, OrderItem
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
