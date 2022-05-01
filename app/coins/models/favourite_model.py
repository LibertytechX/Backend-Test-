from .base_model import BaseModel
from .coin_model import Coin

from django.core.validators import RegexValidator
from django.db import models


# Create your model(s) here.
class FavouriteCoin(BaseModel):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    username = models.CharField(max_length=25)

    favourite = models.CharField(
        max_length=25,
        validators=[RegexValidator('^[A-Z]*$', 'Only uppercase letters allowed')])

    def __str__(self):
        return f'{self.username}: {self.favourite}'

    class Meta:
        verbose_name_plural = 'Favourites'
        ordering = ['-created_at']
