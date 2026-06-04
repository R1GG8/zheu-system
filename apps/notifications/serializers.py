from rest_framework import serializers
from .models import DeviceToken, Notification


class DeviceTokenSerializer(serializers.ModelSerializer):
    # Переопределяем поле как обычный CharField, чтобы убрать встроенную проверку DRF на уникальность
    fcm_token = serializers.CharField()

    class Meta:
        model = DeviceToken
        fields = ["fcm_token", "device_type"]

    def create(self, validated_data):
        user = self.context["request"].user
        token, created = DeviceToken.objects.update_or_create(
            fcm_token=validated_data["fcm_token"],
            defaults={
                "user": user,
                "device_type": validated_data.get("device_type", ""),
            },
        )
        return token


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "title", "body", "is_read", "created_at"]
