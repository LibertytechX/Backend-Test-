"""Manage admin page for main app."""

from django.contrib import admin
from .models import (
    User, Category, Product, Order, Buyer, Seller
)

# Register your models here.


admin.site.site_header = "Inventory Manager Admin"
admin.site.site_title = "Drop it like its hot"
admin.site.index_title = "Inventory Manager"


class UsersAdmin(admin.ModelAdmin):
     list_display = ["username", "role", "email", "phone_no", "first_name"]

admin.site.register(User, UsersAdmin)



class CategoryAdmin(admin.ModelAdmin):
     list_display = ["title", "created_at"]

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
     list_display = ["category", "name", "description", "price","creator", "created_at"]

admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
     list_display = [
          "buyer", "seller", "item", "paid",
          "order_no", "delivered", "price", "completed"
    ]
admin.site.register(Order, OrderAdmin)


admin.site.register(Buyer)
admin.site.register(Seller)


