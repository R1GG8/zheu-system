from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ResidentProfile, EmployeeProfile, Role   # ← добавь Role


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создаём профиль автоматически при создании пользователя"""
    if created:
        if instance.role == Role.RESIDENT:
            ResidentProfile.objects.create(user=instance)
        else:
            EmployeeProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль при обновлении пользователя"""
    if instance.role == Role.RESIDENT:
        if hasattr(instance, 'resident_profile'):
            instance.resident_profile.save()
    else:
        if hasattr(instance, 'employee_profile'):
            instance.employee_profile.save()