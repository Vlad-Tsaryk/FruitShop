from django.db import models


# Create your models here.
class Fruit(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    last_transaction = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["name"]
