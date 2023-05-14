import random

from django.core.management.base import BaseCommand
from fruits.models import Fruit


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Fruit.objects.exists():
            fruits_names = ['Pineapple', 'Apple', 'Banana', 'Orange', 'Apricot', 'Kiwi']
            for fruit_name in fruits_names:
                Fruit.objects.create(
                    name=fruit_name,
                    quantity=random.randrange(10, 100)
                )
            print('*** Fruits created ***')
        else:
            print('*** Fruits already exists ***')
