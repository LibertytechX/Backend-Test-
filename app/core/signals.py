import decimal
from builtins import map, str, float
import os
from django.contrib.auth import get_user_model

User = get_user_model()
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)