from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.time.strftime("%H:%M:%S")} {self.sender.username}: {self.text}\n'

    class Meta:
        ordering = ["-pk"]
