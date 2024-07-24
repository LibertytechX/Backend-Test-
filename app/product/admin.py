from django.contrib import admin
from .models import (Color, Category, Product, 
                     Cart, Cartitems, Order, OrderItems)
# Register your models here.

admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(Order)
admin.site.register(OrderItems)
