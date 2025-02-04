from rest_framework import permissions

class TenantPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role.__eq__("tenan")
    

class InnkeeperPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role.__eq__("innkr")


class AdminPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role.__eq__("admin")