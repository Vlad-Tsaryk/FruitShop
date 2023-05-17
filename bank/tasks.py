from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.core.cache import cache


@shared_task(bind=True)
def task_check_warehouse(self, user_id):
    channel_layer = get_channel_layer()
    for i in range(1, 26):
        math_operations = [11111**111111 for _ in range(20)]
        current_percent = i * 4
        self.update_state(
            state="PROGRESS", meta={"current": current_percent, "total": 100}
        )
        cache.set(f"user_{user_id}_progress", current_percent)
        async_to_sync(channel_layer.group_send)(
            f"chat_audit_{user_id}",
            {"type": "update.progress.bar", "progress": current_percent},
        )
    cache.delete(f"user_{user_id}_progress")
    cache.delete(f"user_{user_id}")
    return {"current": 100, "total": 100}
