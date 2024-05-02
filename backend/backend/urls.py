from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/base/', include('api_base.urls')),
    path('api/lessons/', include('api_lessons.urls')),
    path('api/tasks/', include('api_tasks.urls')),
    path('api/users/', include('api_users.urls')),
]
