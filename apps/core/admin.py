from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Building, Apartment, ResidentProfile, EmployeeProfile


# Регистрируем кастомную модель пользователя
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Что отображать в списке пользователей
    list_display = ("username", "email", "role", "is_staff")
    # Добавляем наши новые поля в формы редактирования
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("role", "phone", "full_name")}),
    )
    # Добавляем поля в форму создания
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("role", "phone", "full_name")}),
    )


# Регистрируем простые модели для домов и квартир
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("address",)


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("building", "number")


# Регистрируем профили
@admin.register(ResidentProfile)
class ResidentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "apartment")


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "position", "department")
