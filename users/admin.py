from django.contrib import admin

from .models import Action, Resource, Permission, Role, CustomUser

admin.site.register(Action)
admin.site.register(Resource)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(CustomUser)
