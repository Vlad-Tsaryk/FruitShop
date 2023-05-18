from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.exists():
            usernames = ["Maria", "Victor", "Bob"]
            for username in usernames:
                User.objects.create_user(username=username, email=f'{username.lower()}@gmail.com',
                                         password='Fruit12345')
            User.objects.create_user('jester')
            print("*** Users created ***")
        else:
            print("*** Users already exists ***")
