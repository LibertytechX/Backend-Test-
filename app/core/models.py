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
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'



class Category(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    in_stock =models.BooleanField(default=True)
    stock_qty=models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class CartItem(models.Model):
    """for user to select product and quantity of that specific product. """
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ordered=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name}-cart-items"

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name}-orders"