from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'paid', 'created_at')
    list_filter = ('status', 'paid', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)