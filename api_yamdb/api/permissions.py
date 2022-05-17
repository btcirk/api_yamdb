from rest_framework import permissions

moderator = ('PATCH', 'DELETE')
moderator_role = ('moderator', 'admin')
admin_role = ('admin',)
authorized_user = ('admin', 'moderator', 'user')


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


# class IsAdminPermission(permissions.BasePermission):
#    def has_permission(self, request, view):
#        if request.user.is_anonymous:
#            return False
#        return request.user.role == 'a'


class IsAdminOrSuperuserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.role in admin_role
                or request.user.is_superuser)


class AuthorizedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.role in authorized_user
                or request.user.is_superuser)
