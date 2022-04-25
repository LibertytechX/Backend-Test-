from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Favourite
from django.core.exceptions import ObjectDoesNotExist


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_favourites(sender, instance, created, **kwargs):
#     try:
#         instance.favourite.save()
#     except ObjectDoesNotExist:
#         Favourite.objects.create(user=instance)