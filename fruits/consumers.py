# chat/consumers.py
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import task_buy_fruits, task_sell_fruits


class FruitConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'fruit_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        fruit_id = int(text_data_json["fruit_id"])
        quantity = int(text_data_json["quantity"])
        if action == 'buy':
            await sync_to_async(task_buy_fruits.apply_async)((fruit_id, quantity))
        elif action == 'sell':
            await sync_to_async(task_sell_fruits.apply_async)((fruit_id, quantity))

    async def fruit_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({"message": message}))


class BankConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'balance_update'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def balance_update(self, event):
        balance = event['balance']
        await self.send(text_data=json.dumps({"balance": balance}))

    async def update_progress_bar(self, event):
        await self.send(text_data=json.dumps({
            "progress": event['progress']
        }))
