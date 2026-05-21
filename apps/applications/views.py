from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer, ApplicationCreateSerializer
from core.models import Role


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def get_queryset(self):
        user = self.request.user

        # Если админ/диспетчер - видит всё
        if user.role == Role.ADMIN:
            return Application.objects.all()

        # Если мастер - видит только те, что назначены на него
        if user.role == Role.MASTER:
            return Application.objects.filter(master=user)

        # Если житель - видит только свои заявки
        return Application.objects.filter(creator=user)

    def perform_create(self, serializer):
        # Принудительно назначаем текущего пользователя создателем
        serializer.save(creator=self.request.user)

    # Дополнительный метод для смены статуса (для мастеров и админов)
    def update(self, request, *args, **kwargs):
        # Тут можно добавить проверку прав:
        # житель не может менять статус, только мастер или админ
        return super().update(request, *args, **kwargs)
