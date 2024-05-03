from django.urls import path
from .views import *

urlpatterns = [
    path('firebase/auth/', FireBaseAuthAPI.as_view(), name='firebase_auth'),
    path("get_welcome_info/", get_welcome_info)
]
