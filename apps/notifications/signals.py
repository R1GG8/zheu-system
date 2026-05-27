from django.db.models.signals import post_save
from django.dispatch import receiver

from applications.models import Application


@receiver(post_save, sender=Application)
def notify_application_update(sender, instance, created, **kwargs):
    if created:
        # Уведомляем админов/диспетчеров о новой заявке (опционально)
        pass
    else:
        # Уведомляем ЖИТЕЛЯ о смене статуса
        from .services import send_push_notification

        send_push_notification(
            user=instance.creator,
            title=f"Заявка №{instance.number}",
            body=f"Статус изменен на: {instance.get_status_display()}",
        )
