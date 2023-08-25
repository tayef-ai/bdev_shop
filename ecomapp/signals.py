from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def saveprofile(sender, instance, **kwargs):
    instance.customer.save()