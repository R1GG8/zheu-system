from rest_framework import permissions
from core.models import Role


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Житель может видеть только свои заявки.
    Мастер/Админ имеют расширенный доступ.
    """

    def has_object_permission(self, request, view, obj):
        # Админ может всё
        if request.user.role == Role.ADMIN:
            return True
        # Мастер может видеть и редактировать только назначенные на него заявки
        if request.user.role == Role.MASTER:
            return obj.master == request.user
        # Житель может видеть и редактировать только свои заявки
        return obj.creator == request.user


class CanChangeStatus(permissions.BasePermission):
    """
    Только Мастер или Админ могут менять статус заявки.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True

        # Если пытаются изменить статус
        if "status" in request.data:
            return request.user.role in [Role.ADMIN, Role.MASTER]

        return True
