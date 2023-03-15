from rest_framework import permissions


def admin_permissions(user):
    """Пользователь админ или суперюзер"""
    return (user.is_admin or user.is_superuser is True)


def staff_permissions(user):
    """Пользователь админ, модератор или суперюзер"""
    return (user.is_admin or user.is_moderator or user.is_superuser is True)


class AdminOnly(permissions.BasePermission):
    """Доступ для админов и суперпользователя"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return admin_permissions(request.user)
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return admin_permissions(request.user)
        return False


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ на изменение для админов и суперпользователя"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return admin_permissions(request.user)
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return admin_permissions(request.user)


class OnlyOwnAccount(permissions.BasePermission):
    """Доступ на изменение собственных объектов"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Доступ к объектам Review и Comment"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or staff_permissions(request.user)
            or obj.author == request.user
        )
