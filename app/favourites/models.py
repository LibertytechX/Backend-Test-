from django.db import models
from django.conf import settings


class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    usd_price = models.CharField(max_length=200, null=True)
    volume = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.name

