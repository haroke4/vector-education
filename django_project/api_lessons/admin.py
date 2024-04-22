from django.contrib import admin
from api_base.admin import UniversalAdmin
from .models import *


admin.site.register(LessonCategory, UniversalAdmin)
admin.site.register(Lesson, UniversalAdmin)
