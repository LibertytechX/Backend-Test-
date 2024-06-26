from django.db import models
from django.contrib.auth import get_user_model

from order.models import TimeStampBaseModel
from product.models import Product

User = get_user_model()


class Order(TimeStampBaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        ordering = ['order', 'product']