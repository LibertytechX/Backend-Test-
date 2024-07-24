from django.dispatch import receiver
from django.contrib.auth.models import User
from customer.models import CustomerDetail
from django.db.models.signals import post_save
 
 
@receiver(post_save, sender=User)
def profileupdate(sender, created, instance, **kwarg):
    if created:
        user = instance
        cutomer = CustomerDetail.objects.create(
            user = user,
        )
        