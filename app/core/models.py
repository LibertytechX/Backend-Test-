from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', default=0,null=True, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='product', through='OrderProduct')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()