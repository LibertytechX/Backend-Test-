from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]
    

class Products(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    price = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]

class OrderedItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        ordering = ["-id"]
    
    

class Order(models.Model):
    items = models.ManyToManyField(OrderedItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]

    @property
    def get_total_price(self):
        return sum([item.quantity * item.product.price for item in self.items.all()])
    
    @property
    def get_total_quantity(self):
        return sum([
            item.quantity for item in self.items.all()
        ])

