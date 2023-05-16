# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/fruits/", consumers.FruitConsumer.as_asgi()),
    re_path(r"ws/balance/", consumers.BankConsumer.as_asgi()),
]