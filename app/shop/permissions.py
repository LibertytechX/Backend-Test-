from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to have full access.
    Other users have read-only access.
    """

    def has_permission(self, request, view):
        # Allow all users to have read-only access
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow only admin users to have full access
        return request.user and request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are only allowed to the owner of the order.
        return obj == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner or admin.
        return obj.user == request.user or request.user.is_staff


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff
