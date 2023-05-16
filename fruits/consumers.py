# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


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