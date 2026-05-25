from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Application, ApplicationStatusHistory


@receiver(pre_save, sender=Application)
def capture_old_status(sender, instance, **kwargs):
    """Сохраняем старый статус перед обновлением"""
    if instance.id:
        try:
            old_instance = Application.objects.get(id=instance.id)
            instance._old_status = old_instance.status
        except Application.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Application)
def log_status_change(sender, instance, created, **kwargs):
    """Записываем изменение в историю, если статус изменился"""
    old_status = getattr(instance, "_old_status", None)

    if created or old_status != instance.status:
        ApplicationStatusHistory.objects.create(
            application=instance,
            from_status=old_status,
            to_status=instance.status,
            # Примечание: changed_by лучше заполнять в ViewSet, так как в сигнале нет доступа к request
        )
