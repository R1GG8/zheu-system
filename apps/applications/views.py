# apps/applications/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models

from .models import Application
from .serializers import ApplicationSerializer, ApplicationCreateSerializer
from core.models import User, Role  # Импортируем User и Role
from .permissions import IsOwnerOrStaff, CanChangeStatus


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff, CanChangeStatus]

    def get_serializer_class(self):
        if self.action == "create":
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == Role.ADMIN:
            return Application.objects.all()

        if user.role == Role.MASTER:
            # Мастер видит свои задачи И все новые (неназначенные), чтобы взять их в работу
            return Application.objects.filter(
                models.Q(master=user) | models.Q(status=Application.Status.NEW)
            )

        return Application.objects.filter(creator=user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # 1. Действие Диспетчера: Назначить мастера
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def assign_master(self, request, pk=None):
        application = self.get_object()
        master_id = request.data.get("master_id")

        try:
            master = User.objects.get(id=master_id, role=Role.MASTER)
            application.master = master
            application.status = Application.Status.IN_PROGRESS
            application.save()
            return Response({"status": "Мастер назначен"})
        except User.DoesNotExist:
            return Response({"error": "Мастер не найден"}, status=400)

    # 2. Действие Мастера: Взять заявку в работу (Самоназначение)
    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def self_assign(self, request, pk=None):
        application = self.get_object()

        if request.user.role != Role.MASTER:
            return Response(
                {"error": "Только мастера могут назначать себя на заявки"}, status=403
            )

        if application.status != Application.Status.NEW:
            return Response(
                {"error": "Заявка уже обрабатывается другим мастером"}, status=400
            )

        application.master = request.user
        application.status = Application.Status.IN_PROGRESS
        application.save()
        return Response({"status": "Вы успешно взяли заявку в работу"})

    # 3. Безопасное изменение статуса (для Мастера и Админа) с комментарием
    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def change_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get("status")
        comment = request.data.get("comment", "")

        if request.user.role != Role.ADMIN and application.master != request.user:
            return Response(
                {"error": "Вы не можете менять статус чужой заявки"}, status=403
            )

        if new_status not in Application.Status.values:
            return Response({"error": "Некорректный статус"}, status=400)

        application.status = new_status
        application.save()  # Сигнал автоматически создаст запись в истории

        # Если мастер оставил комментарий, обновим им запись в истории
        if comment:
            history = application.status_history.order_by("-changed_at").first()
            if history:
                history.comment = comment
                history.changed_by = request.user
                history.save()

        return Response({"status": "Статус успешно изменен"})
