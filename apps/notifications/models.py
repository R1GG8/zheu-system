from django.db import models

from core.models import User


class DeviceToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="device_tokens"
    )
    fcm_token = models.TextField(unique=True)
    device_type = models.CharField(max_length=20, blank=True)  # ios/android
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"
