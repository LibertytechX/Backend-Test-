from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampBaseModel):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    
class Product(TimeStampBaseModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    
    def __str__(self):
        return f"product:-{self.name}: category:{self.category.name}"
    
    class Meta:
        ordering = ['-created_at']