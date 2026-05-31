from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User, ResidentProfile, EmployeeProfile, Role


@receiver(pre_save, sender=User)
def handle_user_pre_save(sender, instance, **kwargs):
    """
    Выполняется ДО сохранения пользователя.
    Идеальное место для изменения полей самого User.
    """
    if instance.is_superuser and instance.role != Role.ADMIN:
        instance.role = Role.ADMIN


@receiver(post_save, sender=User)
def handle_user_profile_sync(sender, instance, created, **kwargs):
    """
    Выполняется ПОСЛЕ сохранения пользователя.
    Создает нужный профиль или обновляет существующий.
    """
    if instance.role == Role.RESIDENT:
        ResidentProfile.objects.get_or_create(user=instance)
        EmployeeProfile.objects.filter(user=instance).delete()

    else:
        profile, is_created = EmployeeProfile.objects.get_or_create(
            user=instance, defaults={"position": instance.get_role_display()}
        )

        if not is_created:
            profile.position = instance.get_role_display()
            profile.save()

        ResidentProfile.objects.filter(user=instance).delete()
