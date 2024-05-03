from django.contrib import admin
from backend.admin import UniversalAdmin
from .models import *


admin.site.register(Lesson, UniversalAdmin)
