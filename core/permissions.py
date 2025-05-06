from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allows access only to users in the 'Admin' group."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()

class IsServiceAdvisor(permissions.BasePermission):
    """Allows access only to users in the 'ServiceAdvisor' group."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='ServiceAdvisor').exists()

class IsTechnician(permissions.BasePermission):
    """Allows access only to users in the 'Technician' group."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Technician').exists()
