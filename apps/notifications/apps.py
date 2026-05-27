import os
from django.apps import AppConfig
from django.conf import settings
import firebase_admin
from firebase_admin import credentials


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"

    def ready(self):
        # Проверяем, не инициализирован ли уже (важно для runserver)
        if not firebase_admin._apps:
            if os.path.exists(settings.FIREBASE_KEY_PATH):
                cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)
                firebase_admin.initialize_app(cred)
            else:
                print("WARNING: Firebase key file not found!")
