import os
import django

# Настройка окружения Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from notifications.services import send_push_notification
from core.models import User


def run_test():
    # Найди своего пользователя (админа)
    user = User.objects.filter(is_superuser=True).first()

    if not user:
        print("Пользователь не найден!")
        return

    print(f"Проверка связи для пользователя: {user.username}")

    # Пытаемся отправить "пустое" уведомление.
    # Оно выдаст ошибку, если ключ неверный,
    # или просто напишет "успешно отправлено 0", если нет токенов.
    try:
        send_push_notification(
            user=user,
            title="Тест системы ЖЭУ",
            body="Если вы это видите, значит Firebase настроен верно!",
        )
        print("---")
        print("Связь с Firebase установлена успешно!")
    except Exception as e:
        print(f"Ошибка конфигурации Firebase: {e}")


if __name__ == "__main__":
    run_test()
