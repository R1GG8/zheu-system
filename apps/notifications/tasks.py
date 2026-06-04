from celery import shared_task
from .services import send_push_notification
from core.models import User

@shared_task
def send_push_notification_task(user_id, title, body, data=None):
    """Фоновая асинхронная задача отправки пуш-уведомления"""
    try:
        user = User.objects.get(id=user_id)
        send_push_notification(user, title, body, data)
        print(f"[Celery] Пуш успешно отправлен пользователю {user.username}")
    except User.DoesNotExist:
        print(f"[Celery Error] Пользователь с ID {user_id} не найден.")