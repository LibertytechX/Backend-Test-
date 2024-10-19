from django.contrib import admin

from orders.models import Order

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "total_amount",
        "status",
        "created_at",
        "order_ref",
    )
    list_filter = ["status"]
    search_fields = (
        "user__username",
        "order_ref",
    )


admin.site.register(Order, OrderAdmin)
