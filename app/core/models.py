"""Create and manage app models and methods."""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


# Create your models here.


class UserManager(BaseUserManager):
    """USER MANAGER CLASS GOING TO MANAGE OUR USER CLASS."""

    def create_user(self, email, password=None, **extra_fields):
        """Create_user method creates and saves new user objects."""
        if not email:
            raise ValueError('User must have valid email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and saves a new super user."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Product Categories"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(decimal_places=2, max_digits=20)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}: Quantity - {self.quantity}"


"""
I added the above model to cater for each product with different quantity on the Order table. 
Customer may want to order product A - 1 quantity, and product B - 3 quantities
"""


# Create an Order model with fields like user (ForeignKey), product (ManyToManyField), quantity, and date.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_detail = models.ManyToManyField(OrderDetail)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}: OrderID - {self.id}"
