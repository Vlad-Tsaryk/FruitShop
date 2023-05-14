import random
from asyncio import sleep

from celery import shared_task


@shared_task()
def task_buy_fruits(email_address, message):
    while True:
        sleep(random.randrange(4, 21))

    """Sends an email when the feedback form has been submitted."""
    # Simulate expensive operation(s) that freeze Django
    send_mail(
        "Your Feedback",
        f"\t{message}\n\nThank you!",
        "support@example.com",
        [email_address],
        fail_silently=False,
    )
