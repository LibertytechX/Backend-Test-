from django.db import models
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
import logging
from django.contrib.auth.models import PermissionsMixin
import traceback
from typing import Any
from django.db import transaction
from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger(__name__)


class CustomUserManager(UserManager):

    # email validator static method
    @staticmethod
    def validate_email(email: str) -> None:
        """
        This method validates the email address of a user.
        """
        try:
            validate_email(email)
        except ValidationError:
            logger.error(traceback.format_exc())
            raise ValidationError({"email": _("Please enter a valid email address.")})

    # create user method
    def create_user(
        self, email: str, username: str, password: str = "", **extra_fields: Any
    ) -> "User":
        """
        This method creates a user with the specified email address, username, and password.
        """
        if not email:
            logger.error(traceback.format_exc())
            raise ValueError("Users must have an email address.")
        if not username:
            logger.error(traceback.format_exc())
            raise ValueError("Users must have a username.")
        with transaction.atomic():
            user = self.model(email=email, username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user


class User(AbstractUser, PermissionsMixin):
    """
    This class maps to users table in database.
    """

    objects = CustomUserManager()
    email = models.EmailField(verbose_name=_("Email address"), unique=True)
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=30,
        unique=True,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    first_name = models.CharField(
        verbose_name=_("First name"), max_length=30, null=True, blank=True
    )
    last_name = models.CharField(
        verbose_name=_("Last name"), max_length=30, null=True, blank=True
    )
    phone_number = PhoneNumberField(blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "users"

    def __str__(self) -> str:
        return f"{self.username} - {self.email}"

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.username}"

    @full_name.setter
    def full_name(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.save()
