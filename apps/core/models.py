from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    RESIDENT = "RESIDENT", _("Житель")
    MASTER = "MASTER", _("Мастер")
    ADMIN = "ADMIN", _("Администратор (Диспетчер)")


class User(AbstractUser):
    """
    Базовая модель пользователя.
    """

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.RESIDENT, verbose_name="Роль"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,  # добавил null=True
        verbose_name="Телефон",
    )
    full_name = models.CharField(max_length=255, blank=True, verbose_name="ФИО")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.full_name or self.username


class Building(models.Model):
    """Модель дома"""

    address = models.CharField(max_length=255, verbose_name="Адрес")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"
        ordering = ["address"]

    def __str__(self):
        return self.address


class Apartment(models.Model):
    """Модель квартиры"""

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="apartments",
        verbose_name="Дом",
    )
    number = models.CharField(max_length=10, verbose_name="Номер квартиры")

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
        unique_together = ("building", "number")  # важно!
        ordering = ["building", "number"]

    def __str__(self):
        return f"{self.building.address}, кв. {self.number}"


class ResidentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="resident_profile",
        verbose_name="Пользователь",
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Квартира",
    )

    class Meta:
        verbose_name = "Профиль жителя"
        verbose_name_plural = "Профили жителей"

    def __str__(self):
        return f"Житель: {self.user.get_full_name() or self.user.username}"


class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        verbose_name="Пользователь",
    )
    position = models.CharField(max_length=100, verbose_name="Должность")
    department = models.CharField(max_length=100, blank=True, verbose_name="Отдел")

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"

    def __str__(self):
        return f"{self.user} — {self.position}"
