from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'apps.core' # Путь до папки для импорта
    label = 'core'     # Короткое имя для связей в базе (как раз для core.User)
    
    def ready(self):
        import apps.core.signals  # noqa