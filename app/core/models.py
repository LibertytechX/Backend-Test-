"""Create and manage app models and methods."""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet
from .utils.db_options import Role
import random
from django.utils import timezone
import string

# Create your models here.



class User(AbstractUser):
    
    Role = Role
    role = models.CharField(max_length=50, choices=Role.choices)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(verbose_name="Phone Number", unique=True, max_length=15)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "phone_no"]


class BuyerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        results =  super().get_queryset(*args, **kwargs)
        return results.filter(role=User.role.BUYER)


class Buyer(User):
    base_role = User.Role.BUYER

    class Meta:
        proxy = True
    buyer = BuyerManager()
    



class SellerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        results =  super().get_queryset(*args, **kwargs)
        return results.filter(role=User.role.SELLER)


class Seller(User):
    base_role = User.Role.SELLER

    class Meta:
        proxy=True
    seller = SellerManager()


class Category(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Job Categories"
        

    def __str__(self):
        return self.title
    


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price  = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    created_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.name
    


def order_number() -> str:
    digits = ''.join(random.choices(string.digits, k=6))
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    order_num = letters + digits
    return order_num
    
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyers")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    paid = models.BooleanField(default=False)
    order_no = models.CharField(default=order_number, max_length=10)
    delivered = models.BooleanField(default=False)
    price = models.PositiveIntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"Order between {self.seller} and {self.buyer}"
    
