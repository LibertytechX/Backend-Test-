from django.contrib import admin
from .models import Category, Product
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name',)

    search_fields = ('name',)

    ordering = ('name',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'stock', 'is_available', 'category')

    list_filter = ('is_available', 'category')

    search_fields = ('name', 'description', 'category__name')

    ordering = ('name',)

    readonly_fields = ('is_available',)


admin.site.register(Product, ProductAdmin)
