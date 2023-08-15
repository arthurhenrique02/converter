from django.db import models


# Create your models here.
class User(models.Model):
    # username
    user = models.CharField(max_length=30, unique=True)
    # user email
    email = models.EmailField(unique=True)
    # user password
    password = models.CharField(max_length=30)
