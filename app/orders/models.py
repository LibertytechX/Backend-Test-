from django.db import models
from products.models import Product
from core.models import User

# Create your models here.


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(choices=(
        ('UNPAID', 'Order is unpaid'),
        ('CANCELED', 'Order was canceled'),
        ('PROCESSING', 'Product has been paid for and is being processed'),
        ('DELIVERED', 'Delivered product'),
    ),
                              max_length=10,
                              default='UNPAID')

    def __str__(self):
        return f"{self.product} - {self.status}"


class Order(models.Model):
    user = models.ForeignKey(User,
                             related_name='orders',
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    date = models.DateTimeField(auto_now_add=True)
