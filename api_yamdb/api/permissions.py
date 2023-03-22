from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Доступ для админов и суперпользователя"""
    message = 'Отказано в доступе'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ на изменение для админов и суперпользователя"""
    message = 'Отказано в доступе'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Доступ к объектам Review и Comment"""
    message = 'Отказано в доступе'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
