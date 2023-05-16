from django.db import models


# Create your models here.
class Bank(models.Model):
    balance = models.IntegerField()
