from django.contrib import admin
from .models import *


class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request, obj=None):
        return [field.name for field in obj.model._meta.fields]


admin.site.register(UserProfile, UniversalAdmin)
admin.site.register(NotificationSettings, UniversalAdmin)
