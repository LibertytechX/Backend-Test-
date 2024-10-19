from django.contrib import admin

from products.models import Category, Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "available_quantity"]
    search_fields = ["name", "price"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
