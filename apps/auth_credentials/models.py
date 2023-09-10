from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.using("auth_db").create(user=instance)


# Create your models here.
class User(models.Model):
    # username
    user = models.CharField(max_length=30, unique=True)
    # user email
    email = models.EmailField(unique=True)
    # user password
    password = models.CharField(max_length=30)
