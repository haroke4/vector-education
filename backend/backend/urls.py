from django.contrib import admin
from django.urls import include, path
from protected_media import urls
from . import protected_media_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_lessons/', include('api_lessons.urls')),
    path('api_am/', include('api_additional_materials.urls')),
    path('api_users/', include('api_users.urls')),
    path('api_dc/', include('api_data_collection.urls')),
    path('api_ge/', include('api_global_event.urls')),
    path('protected/', include(protected_media_view)),

]
