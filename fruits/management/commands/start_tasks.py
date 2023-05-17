from django.core.management import BaseCommand

from fruits.tasks import task_buy_fruits, task_sell_fruits
from users.tasks import task_joker


class Command(BaseCommand):
    def handle(self, *args, **options):
        task_buy_fruits.apply_async(kwargs={'reply': True})
        task_sell_fruits.apply_async(kwargs={'reply': True})
        task_joker.apply_async()