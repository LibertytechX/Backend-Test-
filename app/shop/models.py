import logging
from django.db import IntegrityError, models
from django.core.validators import MinValueValidator
from django.conf import settings

from shop.exceptions import OutOfStocksException
# Create your models here.


class DateTimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f'Category: {self.name}'


class AvailableProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_available=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    price = models.PositiveIntegerField(verbose_name="Price (NGN)")
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(editable=False)

    available = AvailableProductManager()
    objects = models.Manager()

    class Meta:
        ordering = ('name', 'description', 'price')

    def __str__(self):
        return f"Product: {self.name} (NGN {self.price})"

    def save(self, *args, **kwargs):
        # a signal could be better for enterprise level implementations
        self.check_product_inventory()
        super().save(*args, **kwargs)

    def check_product_inventory(self):
        self.is_available = self.stock > 0


class Order(DateTimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItem")
    is_checked_out = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ("created_at", "updated_at")

    def __str__(self):
        return f"Order by {self.user.name}"

    def check_out_order(self):
        self.is_checked_out = True
        self.save(update_fields=["is_checked_out"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # the smallest possible value to order is 1
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return f"Ordered {self.quantity} of {self.product}"

    def save(self, *args, **kwargs):
        self._validate_product_inventory()
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            logging.exception("Product is not available")
            raise OutOfStocksException
        except Exception as e:
            logging.exception("An exception occurred while saving ", e)
            raise e

    def _validate_product_inventory(self):

        if not self.product.is_available:
            logging.exception(
                f"The item {self.product.name} is out of stock")
            raise OutOfStocksException(
                f"The item {self.product.name} is out of stock")
