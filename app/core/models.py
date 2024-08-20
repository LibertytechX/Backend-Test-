"""Create and manage app models and methods."""

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
                                        

from rest_framework_simplejwt.tokens import RefreshToken

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
    
    def get_tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class Category(models.Model):
    """ustom Category model with relations to Product"""
    
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField(max_length=700, null=True)
    
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    """Custom Product model with relations to Category and Order"""
        
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField(max_length=700, null=True)
    price = models.FloatField(null=False, )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=0, null=False)
        
    def __str__(self):
        return self.name

class Order(models.Model):
    """Custom Order model with relations to User and Product"""
    
    class Status(models.TextChoices):
        INITIATED = "INITIATED", "Initiated"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.INITIATED)
    date_created = models.CharField(max_length=50, default=datetime.now(), null=False)
    date_updated = models.CharField(max_length=50, default=datetime.now(), null=True)
    
    class Meta: 
        ordering = ["-date_created"]
    
    def save(self, *args, **kwargs):
        self.date_updated = datetime.now()
        super().save(*args, **kwargs)
    