from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 'customer'  # Default rol
        
        if instance.is_superuser or instance.is_staff:
            role = 'owner'
        else :
            Customer.objects.create(user=instance)
        Profile.objects.create(user=instance, role=role)

    instance.profile.save()


