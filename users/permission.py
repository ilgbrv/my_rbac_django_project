from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from .models import AccessRoleRule

class CustomRBACPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()

        if request.user.is_staff:
            return True

        if not request.user.role:
            raise PermissionDenied(detail="Вам не назначена роль в системе.")

        required_element = getattr(view, 'required_element', None)
        if not required_element:
            raise PermissionDenied(detail="Для этого эндпоинта не настроены правила доступа.")

        try:
            rule = AccessRoleRule.objects.get(role=request.user.role, element_name=required_element)
        except AccessRoleRule.DoesNotExist:
            raise PermissionDenied(detail="У вашей роли нет доступа к этому ресурсу.")

        
        method = request.method # GET, POST, PUT, PATCH, DELETE

        if method == 'GET':
            if rule.read_all_permission or rule.read_permission:
                return True
                
        elif method == 'POST':
            if rule.create_permission:
                return True
                
        elif method in ['PUT', 'PATCH']:
            if rule.update_all_permission or rule.update_permission:
                return True
                
        elif method == 'DELETE':
            if rule.delete_all_permission or rule.delete_permission:
                return True

        raise PermissionDenied(detail="Недостаточно прав для выполнения этого действия.")

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        required_element = getattr(view, 'required_element', None)
        
        try:
            rule = AccessRoleRule.objects.get(role=request.user.role, element_name=required_element)
        except AccessRoleRule.DoesNotExist:
            return False

        method = request.method

        is_owner = getattr(obj, 'owner', None) == request.user or getattr(obj, 'user', None) == request.user

        if method == 'GET':
            if rule.read_all_permission:
                return True
            return rule.read_permission and is_owner

        elif method in ['PUT', 'PATCH']:
            if rule.update_all_permission:
                return True
            return rule.update_permission and is_owner

        elif method == 'DELETE':
            if rule.delete_all_permission:
                return True
            return rule.delete_permission and is_owner

        return False