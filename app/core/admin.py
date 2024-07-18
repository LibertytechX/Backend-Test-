from django.contrib import admin
from core.models import User, ProductCategory, Product, Order, OrderDetail


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_on", "updated_on"]
    list_filter = ["price", "created_on"]
    search_fields = ["name"]


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["user", "created_on", "updated_on"]


admin.site.register(User)
admin.site.register(ProductCategory)
admin.site.register(OrderDetail)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Order, OrderModelAdmin)

