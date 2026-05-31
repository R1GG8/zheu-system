# apps/applications/admin.py
from django.contrib import admin
from .models import Application, ApplicationAttachment, ApplicationStatusHistory


# Позволяет видеть вложенные фото прямо в карточке заявки
class AttachmentInline(admin.TabularInline):
    model = ApplicationAttachment
    extra = 0
    readonly_fields = ("file",)


# Позволяет видеть всю историю изменений прямо внутри заявки
class StatusHistoryInline(admin.TabularInline):
    model = ApplicationStatusHistory
    extra = 0
    can_delete = False
    readonly_fields = (
        "from_status",
        "to_status",
        "changed_at",
        "changed_by",
        "comment",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "creator", "master", "status", "created_at")
    list_filter = ("status", "service_type", "created_at")
    search_fields = (
        "number",
        "title",
        "description",
        "creator__username",
        "creator__full_name",
    )
    readonly_fields = ("number", "created_at", "updated_at")
    inlines = [AttachmentInline, StatusHistoryInline]


# Отдельная регистрация истории для удобного поиска диспетчером
@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "from_status",
        "to_status",
        "changed_by",
        "changed_at",
    )
    list_filter = ("to_status", "changed_at")
    search_fields = ("application__number", "application__title", "comment")
    readonly_fields = ("changed_at",)
