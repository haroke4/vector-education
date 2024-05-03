from django.urls import path
from .views import *

urlpatterns = [
    path("get_lessons/<str:category>/", GetLessons.as_view()),
    path("get_additional_materials/", GetAdditionalMaterials.as_view())
]
