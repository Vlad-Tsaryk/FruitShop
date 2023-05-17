from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='messages', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.time.strftime("%H:%M:%S")} {self.sender.name}: {self.text}'

    class Meta:
        ordering = '-pk'
