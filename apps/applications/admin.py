from django.contrib import admin
from .models import Application, ApplicationAttachment


class AttachmentInline(admin.TabularInline):
    model = ApplicationAttachment
    extra = 1


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "creator", "master", "status", "created_at")
    list_filter = ("status", "service_type", "created_at")
    search_fields = ("number", "title", "description", "creator__full_name")
    inlines = [AttachmentInline]

    # Чтобы номер нельзя было редактировать вручную
    readonly_fields = ("number", "created_at", "updated_at")
