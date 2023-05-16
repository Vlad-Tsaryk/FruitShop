import random
from celery import shared_task
from time import sleep

from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from bank.models import Bank
from fruits.models import Fruit

logger = get_task_logger(__name__)

fruits = Fruit.objects.all()


@shared_task()
def task_buy_fruits(fruit=None, quantity=random.randint(1, 20)):
    price = random.randint(1, 4)
    total_price = quantity * price
    bank = Bank.objects.first()
    balance = bank.balance
    channel_layer = get_channel_layer()
    if not fruit:
        fruit = random.choice(fruits)
    if balance - total_price > 0:
        fruit.quantity += quantity
        fruit.save()
        balance -= total_price
        bank.balance = balance
        bank.save()
        async_to_sync(channel_layer.group_send)(
            'balance_update',
            {
                'type': 'balance.update',
                'balance': balance
            })
        status = 'SUSSES'
        message = f'The supplier has brought {quantity} {fruit.name.lower()}s.' \
                  f'{total_price} USD have been deducted from the account, the purchase is complete.'
    else:
        status = 'ERROR'
        message = f'The supplier has brought {quantity} {fruit.name.lower()}s.' \
                  f' Insufficient funds in the account, the purchase is canceled.'

    async_to_sync(channel_layer.group_send)(
        'fruit_updates',
        {
            'type': 'fruit.update',
            'message': {
                'text': message,
                'status': status
            }
        })


@shared_task()
def task_sell_fruits(fruit=None):
    quantity = random.randint(1, 10)
    price = random.randint(1, 6)
    total_price = quantity * price
    bank = Bank.objects.first()
    balance = bank.balance
    channel_layer = get_channel_layer()
    if not fruit:
        fruit = random.choice(fruits)
    fruit_quantity = fruit.quantity
    if fruit_quantity - quantity >= 0:
        fruit.quantity = fruit_quantity - quantity
        fruit.save()
        balance += total_price
        bank.balance = balance
        bank.save()
        async_to_sync(channel_layer.group_send)(
            'balance_update',
            {
                'type': 'balance.update',
                'balance': balance
            })

        status = 'SUSSES'
        message = f'The buyer bought {quantity} {fruit.name.lower()}s.' \
                  f'{total_price} USD have been credited to the account, the sale is complete.'
    else:
        status = 'ERROR'
        message = f'The supplier has brought {quantity} {fruit.name.lower()}s.' \
                  f' Lack of production, the sale is canceled.'
    async_to_sync(channel_layer.group_send)(
        'fruit_updates',
        {
            'type': 'fruit.update',
            'message': {
                'text': message,
                'status': status
            }
        })
