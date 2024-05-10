from django.contrib import admin
from backend.admin import UniversalAdmin
from .models import UserModel, NotificationSettings


@admin.register(UserModel)
class UserModelAdmin(UniversalAdmin):
    filter_horizontal = ('friends', 'friendship_requests',)
    search_fields = ('name', 'email')

    def get_list_display(self, request):
        return ('name', 'email', 'blocked', 'user_type')


admin.site.register(NotificationSettings, UniversalAdmin)
