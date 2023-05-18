import os

from celery import Celery

from FruitShop import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FruitShop.settings")

app = Celery("FruitShop")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_routes = {
    "fruits.tasks.task_buy_fruits": {"queue": "fruits"},
    "fruits.tasks.task_sell_fruits": {"queue": "fruits"},
    "bank.tasks.task_check_warehouse": {"queue": "warehouse"},
    "users.tasks.task_jester": {"queue": "fruits"},
}
# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.CELERY_TIMEZONE = "UTC"
