from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners to access the view.
    """

    def has_permission(self, request, view):
        return request.user.role == 'Owner'


class IsTenant(BasePermission):
    """
    Custom permission to only allow tenants to access the view.
    """

    def has_permission(self, request, view):
        return request.user.role == 'Tenant'


class IsAgent(BasePermission):
    """
    Custom permission to only allow agents to access the view.
    """

    def has_permission(self, request, view):
        return request.user.role == 'Agent'
