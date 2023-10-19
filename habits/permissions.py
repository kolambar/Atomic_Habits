from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь создателем объекта
        return obj.owner == request.user
