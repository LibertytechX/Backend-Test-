from django.db import models
from django.contrib.auth.models import User
from User_App.models import CustomUser
# Create your models here.

class Category(models.Model):
    """Define parameters for creating product catergory

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    title = models.CharField(max_length=255, null=False)
    Description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title


class Products(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    Name = models.CharField(max_length=100)
    Description = models.TextField(blank=True, null=True)
    Category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    Price = models.FloatField(null=False)
    Stock = models.FloatField(null=False)
    imageUrl = models.URLField()
    #Created_by = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE)
    Updated_at = models.DateField(auto_now=True)
    Date_created = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['Date_created']

    def __str__(self):
        return '{} {}'.format(self.Price, self.name)


