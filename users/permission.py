from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

class CustomRBACPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()

        if request.user.is_staff:
            return True

        required_resource = getattr(view, 'required_resource', None)
        required_action = getattr(view, 'required_action', None)

        if not required_resource or not required_action:
                raise PermissionDenied()

        user_has_permission = request.user.roles.filter(
                permissions__resource__resource_name=required_resource,
                permissions__action__action_name=required_action
            ).exists()

        if not user_has_permission:
            raise PermissionDenied()

        return True