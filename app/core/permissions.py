from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):
    """ Allow owner only to update records. """

    message = 'You do not have permissions to update this record'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user or request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create and modify objects.
    """

    message = 'Staff level or higher is required to update records'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow write actions for admin users
        return request.user and request.user.is_staff
