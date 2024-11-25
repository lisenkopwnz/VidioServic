from rest_framework.permissions import BasePermission, SAFE_METHODS


class ContentViewSetPermissions(BasePermission):

    def has_permission(self, request, view):
        match request.method:
            case 'GET':
                return True
            case 'POST' | 'PUT' | 'DELETE':
                return request.user and request.user.is_authenticated
            case _:
                return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # Методы записи разрешены только владельцу или администратору
        return obj.author == request.user or request.user.is_staff