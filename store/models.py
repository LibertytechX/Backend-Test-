from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    class PRODUCT_STATUS(models.TextChoices):
        AVAILABLE = "Available", "available"
        UNAVAILABLE = "Unavailable", "unavailable"

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(
        default="AVAILABLE", max_length=15, choices=PRODUCT_STATUS.choices
    )
    added = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def getOrders(self):
        query_order = Order.objects.filter(product_id=self.id).select_related("product")
        return query_order


class Order(models.Model):
    for_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.CASCADE,
        null=True,
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE, null=True
    )
    quantity = models.PositiveIntegerField(default=1)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
