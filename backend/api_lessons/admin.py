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
    class QuestionInline(admin.TabularInline):
        model = Question
        extra = 0
        fields = ('text',)

    list_display = ('id', 'lesson_batch', 'topic', 'description', 'video_url')
    search_fields = list_display

    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    class QuestionAnswerInline(admin.TabularInline):
        model = QuestionAnswer
        extra = 0
        fields = ('text', 'is_correct')

    list_display = ('id', 'lesson', 'text')
    search_fields = list_display

    inlines = [QuestionAnswerInline]


admin.site.register(QuestionAnswer)
