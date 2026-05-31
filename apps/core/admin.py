from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Building, Apartment, ResidentProfile, EmployeeProfile


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("address", "created_at")
    search_fields = ("address",)


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("building", "number")
    list_filter = ("building",)
    search_fields = ("number", "building__address")


@admin.register(ResidentProfile)
class ResidentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "apartment")
    search_fields = ("user__username", "user__full_name", "apartment__number")


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "position", "department", "is_active_worker")
    list_filter = ("is_active_worker", "department")
    search_fields = ("user__username", "user__full_name", "position")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("role", "phone", "full_name")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("role", "phone", "full_name", "email")}),
    )
    list_display = ["username", "email", "full_name", "role", "is_staff"]
