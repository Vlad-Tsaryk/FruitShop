from django.core.management.base import BaseCommand

from bank.models import Bank


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Bank.objects.exists():
            Bank.objects.create(balance=10000)
            print("*** Bank created ***")
        else:
            print("*** Bank already exists ***")
