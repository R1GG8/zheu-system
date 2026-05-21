from rest_framework import serializers
from .models import Application, ApplicationAttachment
from core.models import User


# Сериализатор для вложений
class ApplicationAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationAttachment
        fields = ["id", "file", "uploaded_at"]


# Основной сериализатор для просмотра заявок
class ApplicationSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField(source="creator.full_name")
    master_name = serializers.ReadOnlyField(source="master.full_name")
    attachments = ApplicationAttachmentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    service_type_display = serializers.CharField(
        source="get_service_type_display", read_only=True
    )

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
        ]
        read_only_fields = ["number", "creator", "status", "created_at", "updated_at"]


# Сериализатор специально для создания заявки жителем
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["title", "description", "service_type"]

    def create(self, validated_data):
        # Логика автоматического назначения создателя будет в ViewSet
        return super().create(validated_data)
