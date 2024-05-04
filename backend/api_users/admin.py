from django.contrib import admin
from backend.admin import UniversalAdmin
from .models import UserModel, NotificationSettings

admin.site.register(UserModel, UniversalAdmin)
admin.site.register(NotificationSettings, UniversalAdmin)
