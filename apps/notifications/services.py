import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings


def send_push_notification(user, title, body, data=None):
    """Отправка уведомления на все устройства пользователя"""
    tokens = list(user.device_tokens.values_list("fcm_token", flat=True))

    if not tokens:
        return

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        tokens=tokens,
    )

    response = messaging.send_multicast(message)
    print(f"Successfully sent {response.success_count} messages")
