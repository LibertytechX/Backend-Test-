from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Check whether the request is from the owner
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only method for everyone
            return True
        # check if the user making the request is the owner
        return obj.user == request.user