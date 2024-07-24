from django.db import models
from User_App.models import CustomUser
from products_App.models import Products
# Create your models here.
class Order(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    Order_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Products)
    

    class Meta:
        ordering = ['Order_id', '-created_at']
        

    def __str__(self):
        return f'{self.Order_id}'
