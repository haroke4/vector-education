from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_lessons/', include('api_lessons.urls')),
    path('api_tasks/', include('api_tasks.urls')),
    path('api_users/', include('api_users.urls')),
]
