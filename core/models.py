"""Create and manage app models and methods."""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)
from django.conf import settings

# Create your models here.


class UserManager(BaseUserManager):
    """USER MANAGER CLASS GOING TO MANAGE OUR USER CLASS."""

    def create_user(self, email, password=None, **extra_fields):
        """Create_user method creates and saves new user objects."""
        if not email:
            raise ValueError("User must have valid email address")

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

    USERNAME_FIELD = "email"


class UserBio(models.Model):
    for_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userbio", on_delete=models.CASCADE
    )
    address = models.CharField(default="No.2 Ally lane...", max_length=255, blank=True)
    address2 = models.CharField(
        default="No.2 JohnDoe Close...", max_length=255, blank=True
    )
    tel = models.CharField(default="", max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user)
