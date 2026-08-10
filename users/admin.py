from django.contrib import admin

from .models import Role, AccessRoleRule, CustomUser

admin.site.register(Role)
admin.site.register(AccessRoleRule)
admin.site.register(CustomUser)
