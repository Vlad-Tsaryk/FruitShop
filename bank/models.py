from django.db import models


# Create your models here.
class Bank(models.Model):
    balance = models.IntegerField()


class Declaration(models.Model):
    date = models.DateField(auto_now=True)
    file = models.FileField(upload_to='declarations')
