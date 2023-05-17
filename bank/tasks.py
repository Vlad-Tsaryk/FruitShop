from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer


@shared_task(bind=True)
def task_check_warehouse(self):
    channel_layer = get_channel_layer()
    for i in range(1, 26):
        math_operations = [11111 ** 111111 for x in range(50)]
        current_percent = i * 4
        self.update_state(state='PROGRESS', meta={'current': current_percent, 'total': 100})
        # cache.set(f'user_progress', current_percent)
        async_to_sync(channel_layer.group_send)(
            f'balance_update',
            {
                "type": "update.progress.bar",
                "progress": current_percent
            }
        )
    # cache.delete(f'user_progress')
    # cache.delete(f'user')
    return {'current': 100, 'total': 100}
