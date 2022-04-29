from .base_model import BaseModel

from django.core.validators import RegexValidator
from django.db import models


# Create your model(s) here.
class Coin(BaseModel):
    name = models.CharField(
        max_length=25,
        validators=[RegexValidator('^[A-Z]*$', 'Only uppercase letters allowed')])

    usd_price = models.CharField(max_length=25)
    volume = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.name} @ {self.usd_price}: {self.volume}'

    class Meta:
        verbose_name_plural = 'Coins'
        ordering = ['-created_at']
