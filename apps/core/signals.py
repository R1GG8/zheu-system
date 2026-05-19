from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ResidentProfile, EmployeeProfile, Role


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Если это суперюзер, принудительно ставим роль ADMIN
        if instance.is_superuser and instance.role != Role.ADMIN:
            instance.role = Role.ADMIN
            instance.save()  # Сохраняем изменение роли

        # Теперь создаем профиль на основе роли
        if instance.role == Role.RESIDENT:
            ResidentProfile.objects.get_or_create(user=instance)
        else:
            EmployeeProfile.objects.get_or_create(
                user=instance, position=instance.get_role_display()
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == Role.RESIDENT:
        if hasattr(instance, "resident_profile"):
            instance.resident_profile.save()
    else:
        if hasattr(instance, "employee_profile"):
            instance.employee_profile.save()


@receiver(post_save, sender=User)
def manage_user_profiles(sender, instance, created, **kwargs):
    """
    Синхронизирует профили при создании или изменении роли пользователя.
    """
    if instance.role == Role.RESIDENT:
        # Создаем профиль жителя, если его нет
        ResidentProfile.objects.get_or_create(user=instance)
    else:
        # Для ADMIN и MASTER создаем профиль сотрудника
        EmployeeProfile.objects.get_or_create(
            user=instance, defaults={"position": instance.get_role_display()}
        )
