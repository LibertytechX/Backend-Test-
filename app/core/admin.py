
from django.contrib import admin
from .models import Category, Product, Order, OrderProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 20

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    ordering = ('name',)
    list_per_page = 20

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date')
    search_fields = ('user__username',)  #Here, I Used related field lookup for search
    list_filter = ('date',)
    ordering = ('-date',)
    list_per_page = 20

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order', 'product')
    ordering = ('order', 'product')
    list_per_page = 20

