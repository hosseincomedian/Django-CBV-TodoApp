from rest_framework import permissions

class IsTodoUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user==obj.user or request.method in permissions.SAFE_METHODS: 
            return True
        return False