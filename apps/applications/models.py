import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models import User

import random


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", _("Новая")
        IN_PROGRESS = "IN_PROGRESS", _("В работе")
        PENDING = "PENDING", _("Ожидает запчастей")
        DONE = "DONE", _("Выполнена")
        CANCELED = "CANCELED", _("Отменена")

    class ServiceType(models.TextChoices):
        PLUMBER = "PLUMBER", _("Сантехник")
        ELECTRICIAN = "ELECTRICIAN", _("Электрик")
        OTHER = "OTHER", _("Другое")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=20, unique=True, verbose_name="Номер заявки")

    # Кто создал (Житель)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_applications",
        limit_choices_to={"role": "RESIDENT"},
        verbose_name="Заявитель",
    )

    # Кто выполняет (Мастер)
    master = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        limit_choices_to={"role": "MASTER"},
        verbose_name="Мастер",
    )

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание проблемы")
    service_type = models.CharField(
        max_length=20,
        choices=ServiceType.choices,
        default=ServiceType.OTHER,
        verbose_name="Тип услуги",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW, verbose_name="Статус"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"№{self.number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.number:
            # Получаем текущее время прямо сейчас
            now = timezone.now()
            # Генерируем номер в формате: ГГГГ-ММ-РАНДОМ (например, 2026-05-1234)
            random_part = random.randint(100, 999)
            self.number = f"{now.year}-{now.month:02d}-{now.day}--{random_part}"

        super().save(*args, **kwargs)


class ApplicationAttachment(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="applications/attachments/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"


class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="status_history",
        verbose_name="Заявка",
    )
    from_status = models.CharField(
        max_length=20, verbose_name="Старый статус", null=True
    )
    to_status = models.CharField(max_length=20, verbose_name="Новый статус")
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="Кто изменил"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "История статуса"
        verbose_name_plural = "История статусов"
