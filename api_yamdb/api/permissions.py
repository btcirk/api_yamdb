from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'a'
        )
