from django.contrib import admin
from .models import Category, Product, Order

# Register the Category model
admin.site.register(Category)

# Customize the admin interface for the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)

# Register the Product model with the customized admin interface
admin.site.register(Product, ProductAdmin)

# Customize the admin interface for the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'quantity')
    list_filter = ('date',)
    search_fields = ('user__username',)

# Register the Order model with the customized admin interface
admin.site.register(Order, OrderAdmin)