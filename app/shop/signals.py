from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def reduce_product_stock_on_save(instance: OrderItem, *args, **kwargs):
    with transaction.atomic():

        instance.product.stock -= instance.quantity
        instance.product.save()  # reduce the product stock


@receiver(post_delete, sender=OrderItem)
def increase_product_stock_on_delete(instance: OrderItem, *args, **kwargs):
    with transaction.atomic():
        instance.product.stock += instance.quantity
        instance.product.save()  # reduce the product stock
