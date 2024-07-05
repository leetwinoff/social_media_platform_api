from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if (
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or (request.user and request.user.is_staff):
            return True
        if view.action in ["update", "partial_update", "destroy"]:
            object = view.get_object()
            if hasattr(object, "user") and object.user == request.user:
                return True
        return False
