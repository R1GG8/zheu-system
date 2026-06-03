import firebase_admin
from firebase_admin import credentials, messaging
from .models import Notification


def send_push_notification(user, title, body, data=None):
    """Отправка уведомления на все зарегистрированные устройства пользователя"""
    if not firebase_admin._apps:
        print("Firebase не инициализирован.")
        return

    tokens = list(user.device_tokens.values_list("fcm_token", flat=True))

    if not tokens:
        print(f"У пользователя {user.username} нет активных токенов устройств.")
        return

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        tokens=tokens,
    )

    Notification.objects.create(user=user, title=title, body=body)
    response = messaging.send_each_for_multicast(message)
    print(f"Successfully sent {response.success_count} messages")
