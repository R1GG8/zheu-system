# apps/applications/permissions.py
from rest_framework import permissions
from core.models import Role


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Диспетчер видит и может редактировать всё
        if request.user.role == Role.ADMIN:
            return True

        # Мастер видит свои заявки ИЛИ новые неназначенные (чтобы взять в работу)
        if request.user.role == Role.MASTER:
            return obj.master == request.user or obj.status == "NEW"

        # Житель видит только свои заявки
        return obj.creator == request.user


class CanChangeStatus(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if "status" in request.data:
            return request.user.role in [Role.ADMIN, Role.MASTER]
        return True
