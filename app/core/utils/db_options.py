from django.db import models



class Role(models.TextChoices):
    SELLER = "SELLER", "Seller"
    BUYER = "BUYER", "Buyer"