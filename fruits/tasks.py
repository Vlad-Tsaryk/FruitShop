import datetime
import random

from asgiref.sync import async_to_sync
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer

from bank.models import Bank
from fruits.models import Fruit

logger = get_task_logger(__name__)

fruits = Fruit.objects.all()


@shared_task(bind=True)
def task_buy_fruits(
        self, fruit_id: int = None, quantity: int = random.randint(1, 20), reply=False
):
    price = random.randint(1, 4)
    total_price = quantity * price
    bank = Bank.objects.first()
    balance = bank.balance
    channel_layer = get_channel_layer()
    if not fruit_id:
        fruit = random.choice(fruits)
    else:
        fruit = Fruit.objects.get(id=fruit_id)
    fruit_name = fruit.name.lower()
    if balance - total_price > 0:
        fruit.quantity += quantity
        fruit.last_transaction = (
            f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'
            f" bought {quantity} {fruit_name}s for {total_price}USD"
        )
        fruit.save()
        balance -= total_price
        bank.balance = balance
        bank.save()
        async_to_sync(channel_layer.group_send)(
            "fruit_updates", {"type": "balance.update", "balance": balance}
        )
        status = "SUSSES"
        message = (
            f"The supplier has brought {quantity} {fruit_name}s."
            f"{total_price} USD have been deducted from the account, the purchase is complete."
        )
    else:
        status = "ERROR"
        message = (
            f"The supplier has brought {quantity} {fruit_name}s."
            f" Insufficient funds in the account, the purchase is canceled."
        )

    async_to_sync(channel_layer.group_send)(
        "fruit_updates",
        {"type": "fruit.update", "message": {"text": message, "status": status, 'fruit_id': fruit.id,
                                             'quantity': fruit.quantity}},
    )
    if reply:
        task_buy_fruits.apply_async(
            countdown=random.randrange(5, 20), kwargs={"reply": True}
        )


@shared_task(bind=True)
def task_sell_fruits(
        self, fruit_id: int = None, quantity: int = random.randint(1, 10), reply=False
):
    price = random.randint(1, 6)
    total_price = quantity * price
    bank = Bank.objects.first()
    balance = bank.balance
    channel_layer = get_channel_layer()
    if not fruit_id:
        fruit = random.choice(fruits)
    else:
        fruit = Fruit.objects.get(id=fruit_id)
    fruit_name = fruit.name.lower()
    fruit_quantity = fruit.quantity
    if fruit_quantity - quantity >= 0:
        fruit.quantity = fruit_quantity - quantity
        fruit.last_transaction = (
            f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'
            f" sold {quantity} {fruit_name}s for {total_price}USD"
        )
        fruit.save()
        balance += total_price
        bank.balance = balance
        bank.save()
        async_to_sync(channel_layer.group_send)(
            "fruit_updates", {"type": "balance.update", "balance": balance}
        )

        status = "SUSSES"
        message = (
            f"The buyer bought {quantity} {fruit_name}s."
            f"{total_price} USD have been credited to the account, the sale is complete."
        )
    else:
        status = "ERROR"
        message = (
            f"The supplier has brought {quantity} {fruit_name}s."
            f" Lack of production, the sale is canceled."
        )
    async_to_sync(channel_layer.group_send)(
        "fruit_updates",
        {"type": "fruit.update", "message": {"text": message, "status": status, 'fruit_id': fruit.id,
                                             'quantity': fruit_quantity - quantity}},
    )
    if reply:
        task_sell_fruits.apply_async(
            countdown=random.randrange(15, 30), kwargs={"reply": True}
        )
