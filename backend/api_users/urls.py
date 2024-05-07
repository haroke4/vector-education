from django.urls import path
from .views import *

urlpatterns = [
    path('auth/', AuthViaFirebase.as_view()),
    path('get_user/', GetUserView.as_view()),
    path("edit_name_description/", EditNameOrDescriptionView.as_view()),
]
