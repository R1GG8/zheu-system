from rest_framework import serializers
from .models import Application, ApplicationAttachment, ApplicationStatusHistory
from core.models import User


class ApplicationAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAttachment
        fields = ["id", "file", "uploaded_at"]


# 1. Создаем сериализатор для истории статусов
class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatusHistory
        fields = ["id", "from_status", "to_status", "changed_at", "comment"]


class ApplicationSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField(source="creator.full_name")
    master_name = serializers.ReadOnlyField(source="master.full_name")
    attachments = ApplicationAttachmentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    service_type_display = serializers.CharField(
        source="get_service_type_display", read_only=True
    )

    # 2. Вкладываем историю в основную заявку
    status_history = ApplicationStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "number",
            "title",
            "description",
            "service_type",
            "service_type_display",
            "status",
            "status_display",
            "creator",
            "creator_name",
            "master",
            "master_name",
            "created_at",
            "updated_at",
            "attachments",
            "status_history",  # <-- Добавили поле в API!
        ]
        read_only_fields = ["number", "creator", "status", "created_at", "updated_at"]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Application
        fields = ["title", "description", "service_type", "uploaded_images"]

    def create(self, validated_data):
        images = validated_data.pop("uploaded_images", [])
        application = Application.objects.create(**validated_data)
        for image in images:
            ApplicationAttachment.objects.create(application=application, file=image)
        return application
