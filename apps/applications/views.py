from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action

from .permissions import CanChangeStatus, IsOwnerOrStaff
from .models import Application
from .serializers import ApplicationSerializer, ApplicationCreateSerializer
from core.models import Role


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()

    parser_classes = [MultiPartParser, FormParser, JSONParser]

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

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def assign_master(self, request, pk=None):
        """Метод для диспетчера: назначить мастера на заявку"""
        application = self.get_object()
        master_id = request.data.get("master_id")

        try:
            master = User.objects.get(id=master_id, role=Role.MASTER)
            application.master = master
            application.status = Application.Status.IN_PROGRESS
            application.save()

            # Сюда можно добавить уведомление мастеру, что ему упала задача
            return Response({"status": "Мастер назначен"})
        except User.DoesNotExist:
            return Response({"error": "Мастер не найден"}, status=400)

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff, CanChangeStatus]
