from rest_framework import viewsets, permissions
from .models import DeviceToken
from .serializers import DeviceTokenSerializer


class DeviceTokenViewSet(viewsets.ModelViewSet):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Пользователь видит только свои токены
        return DeviceToken.objects.filter(user=self.request.user)
