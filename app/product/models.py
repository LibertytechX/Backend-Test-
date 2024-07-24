from typing import Iterable
from django.db import models
import uuid
from django.contrib.auth.models import User

class Color(models.Model):
    color = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return str(self.color)
    
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        self.color = self.color.lower()
        return super().save()

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)
    
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        self.name = self.name.lower()
        return super().save()

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    in_stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.IntegerField()
    colors = models.ManyToManyField(Color, blank=True)
    amount_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owner.username)
    
    @property
    def grandtotal(self):
        cartitems = self.cartitems.all()
        grandtotal = sum([item.price for item in cartitems])
        return grandtotal

    @property
    def numberofitem(self):
        numberofitem = self.cartitems.count()
        return numberofitem


class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.product)
    
    @property
    def price(self):
        final_price = self.quantity * self.product.price
        return final_price
  

class Order(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) 
    is_verified = models.BooleanField(default=False)
    order_id = models.CharField(max_length=13, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.order_id}'
    
    @property
    def grandtotal(self):
        orderitems = self.orderitems.all()
        grandtotal = sum([item.price for item in orderitems])
        return grandtotal

    @property
    def numberofitem(self):
        numberofitem = self.orderitems.count()
        return numberofitem

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        if not self.order_id:
            self.order_id = str(uuid.uuid4().hex[:12].upper())
        return super().save()
    
    def verified(self):
        self.is_verified = True
        self.save()

    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    
    @property
    def price(self):
        final_price = self.quantity * self.product.price
        return final_price
    
    def __str__(self) -> str:
        return f'{self.order.order_id} - {self.order.numberofitem}'