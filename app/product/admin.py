from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id",'name', 'price', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    fields = ('name', 'description', 'price', 'category', 'image')
    list_editable = ('name','price', 'category')

admin.site.register(Product, ProductAdmin)