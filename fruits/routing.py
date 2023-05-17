# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/fruits/", consumers.FruitConsumer.as_asgi()),
    path(r"ws/audit/<int:id>/", consumers.BankConsumer.as_asgi()),
    path(r"ws/chat/", consumers.ChatConsumer.as_asgi()),
]
