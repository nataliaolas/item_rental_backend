from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Uzytkownik

# @receiver(post_save, sender=User)
# def create_user_uzytkownika(sender, instance, created, **kwargs):
#     if created:
#        Uzytkownik.objects.create(user=instance)
#     instance.uzytkownik.save()
