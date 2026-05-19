from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core' # Путь до папки для импорта
    
    def ready(self):
        import core.signals  # noqa