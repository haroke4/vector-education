from django.contrib import admin
from .models import *


@admin.register(LessonBatch)
class LessonBatchAdmin(admin.ModelAdmin):
    class LessonsInline(admin.TabularInline):
        model = Lesson
        extra = 0
        fields = ('topic', 'description', 'video_url',)
        show_change_link = True

    list_display = ('id', 'title')
    search_fields = list_display
    inlines = [LessonsInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    class LessonComponentInline(admin.TabularInline):
        model = LessonComponent
        extra = 0
        fields = ('type', 'video_component', 'question_component', 'conspectus_component', 'order')

    list_display = ('id', 'lesson_batch', 'topic',)
    search_fields = list_display
    inlines = [LessonComponentInline]


@admin.register(LessonComponent)
class LessonComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'type')
    search_fields = list_display


@admin.register(VideoComponent)
class VideoComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'video_url')
    search_fields = list_display


@admin.register(ConspectusComponent)
class ConspectusComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = list_display


@admin.register(QuestionComponent)
class QuestionAdmin(admin.ModelAdmin):
    class QuestionAnswerInline(admin.TabularInline):
        model = QuestionAnswer
        extra = 0
        fields = ('text', 'is_correct')

    list_display = ('id', 'text')
    search_fields = list_display

    inlines = [QuestionAnswerInline]


admin.site.register(QuestionAnswer)
