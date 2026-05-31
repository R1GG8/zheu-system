# apps/notifications/admin.py
from django.contrib import admin
from .models import DeviceToken


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "device_type", "fcm_token", "created_at")
    list_filter = ("device_type", "created_at")
    search_fields = ("user__username", "user__full_name", "fcm_token")
    readonly_fields = ("created_at",)
