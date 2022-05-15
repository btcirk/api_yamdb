from rest_framework import permissions

moderator = ('PATCH', 'DEL')
moderator_role = ('u', 'a')
admin_role = ('a',)


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        moderate = ((request.user.role in moderator_role)
                    and (request.method in moderator))
        return obj.author == request.user or moderate


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class OpenAll(permissions.BasePermission):

    def has_permission(self, request, view):
        return True


class OnlyAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role in admin_role))


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role in admin_role)
