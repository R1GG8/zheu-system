import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User


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
            # Простая генерация номера: год-месяц-рандом
            import random

            self.number = f"{self.created_at.year if self.created_at else '2024'}-{random.randint(1000, 9999)}"
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
