from rest_framework import serializers
from .models import DeviceToken


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ["fcm_token", "device_type"]

    def create(self, validated_data):
        # Привязываем токен к текущему залогиненному пользователю
        user = self.context["request"].user
        # Обновляем, если такой токен уже был, или создаем новый
        token, created = DeviceToken.objects.update_or_create(
            fcm_token=validated_data["fcm_token"],
            defaults={
                "user": user,
                "device_type": validated_data.get("device_type", ""),
            },
        )
        return token
