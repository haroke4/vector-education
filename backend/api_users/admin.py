from django.contrib import admin
from backend.admin import UniversalAdmin
from .models import UserProfile, NotificationSettings

admin.site.register(UserProfile, UniversalAdmin)
admin.site.register(NotificationSettings, UniversalAdmin)
