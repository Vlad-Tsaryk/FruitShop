import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

from users.models import Message


@shared_task(bind=True)
def task_jester(self):
    channel_layer = get_channel_layer()
    jester = User.objects.get(username='jester')

    response = requests.get('https://v2.jokeapi.dev/joke/Any?type=single')
    joke = response.json().get('joke')
    while len(joke) > 255:
        response = requests.get('https://v2.jokeapi.dev/joke/Any?type=single')
        joke = response.json().get('joke')

    joke_message = Message.objects.create(sender=jester, text=joke)
    async_to_sync(channel_layer.group_send)(
        'chat',
        {
            "type": "chat_message",
            "message": str(joke_message),
        }
    )
    task_jester.apply_async(countdown=len(joke))

    # schedule, created = IntervalSchedule.objects.get_or_create(
    #     every=len(joke),
    #     period=IntervalSchedule.SECONDS,
    # )
    # task = PeriodicTask.objects.get(task='users.tasks.task_jester')
    # task.interval = schedule
    # task.save()
    # PeriodicTasks.changed(task)

    return joke
