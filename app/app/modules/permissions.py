from rest_framework.permissions import BasePermission
from customer.models import CustomerDetail


class IsAgentAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user_detail = CustomerDetail.objects.get(user=request.user)
        except CustomerDetail.DoesNotExist:
            return False
        if user_detail.role == "agent":
            return True
        else:
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user_detail = CustomerDetail.objects.get(user=request.user)
        except CustomerDetail.DoesNotExist:
            return False
        if user_detail.role == "admin":
            return True
        else:
            return False