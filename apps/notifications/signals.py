from django.db.models.signals import post_save
from django.dispatch import receiver
from applications.models import Application
from news.models import News
from core.models import User, Role
from .services import send_push_notification


@receiver(post_save, sender=Application)
def notify_application_update(sender, instance, created, **kwargs):
    if created:
        if instance.master:
            send_push_notification(
                user=instance.master,
                title="Предложена новая заявка",
                body=f"Житель предложил вам заявку №{instance.number}: {instance.title}. Ожидает вашего согласия.",
            )
    else:
        send_push_notification(
            user=instance.creator,
            title=f"Заявка №{instance.number}",
            body=f"Статус изменен на: {instance.get_status_display()}",
        )


@receiver(post_save, sender=News)
def notify_new_news(sender, instance, created, **kwargs):
    if created and instance.is_published:
        residents = User.objects.filter(role=Role.RESIDENT)
        for resident in residents:
            send_push_notification(
                user=resident, title="Новое объявление ЖЭУ", body=instance.title
            )
