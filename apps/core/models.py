from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Базовая модель пользователя.
    Здесь хранятся данные для входа и общая информация.
    """

    class Role(models.TextChoices):
        RESIDENT = "RESIDENT", "Житель"
        MASTER = "MASTER", "Мастер"
        ADMIN = "ADMIN", "Администратор (Диспетчер)"

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.RESIDENT, verbose_name="Роль"
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    full_name = models.CharField(max_length=255, blank=True, verbose_name="ФИО")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Building(models.Model):
    """Модель дома"""

    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return self.address


class Apartment(models.Model):
    """Модель квартиры"""

    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name="apartments"
    )
    number = models.CharField(max_length=10, verbose_name="Номер квартиры")

    def __str__(self):
        return f"{self.building.address}, кв. {self.number}"


class ResidentProfile(models.Model):
    """
    Профиль жителя. Связан с User связью "Один-к-Одному".
    Стрелочка на твоей диаграмме — это и есть OneToOneField.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="resident_profile"
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.SET_NULL, null=True, verbose_name="Квартира"
    )

    def __str__(self):
        return f"Профиль жителя: {self.user.username}"


class EmployeeProfile(models.Model):
    """Профиль сотрудника (Мастера или Админа)"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_profile"
    )
    position = models.CharField(max_length=100, verbose_name="Должность")
    department = models.CharField(max_length=100, verbose_name="Отдел")

    def __str__(self):
        return f"Профиль сотрудника: {self.user.username}"
