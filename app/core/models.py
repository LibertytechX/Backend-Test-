"""Create and manage app models and methods."""

from django.db import models
from django.conf import settings
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
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username
    

class Coins(models.Model):
    
    name = models.CharField(max_length=20, db_index=True, unique=True )
    price_usd = models.FloatField()
    volume = models.FloatField()
    

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Favourite(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribed_favourites', on_delete=models.CASCADE, )
    favourite = models.ForeignKey(Coins, related_name='favouritecoin', on_delete=models.CASCADE, db_index=True)
    
    class Meta:
        ordering = ['user']