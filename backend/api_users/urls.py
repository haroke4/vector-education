from django.urls import path
from .views import *

urlpatterns = [
    path('auth/', AuthViaFirebase.as_view()),
    path("get_welcome_info/", get_welcome_info)
]
