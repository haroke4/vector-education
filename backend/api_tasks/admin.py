from django.contrib import admin
from .models import *


@admin.register(UserTasksProfile)
class UserTasksProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile', 'survey_completed',
                    'earned_coins', 'curr_streak', 'max_streak')
    search_fields = ('user_profile__user__username',)
    filter_horizontal = ('completed_quizzes',)


@admin.register(QuizBatch)
class QuizBatchAdmin(admin.ModelAdmin):
    class QuestionsInline(admin.TabularInline):
        model = QuizQuestion
        extra = 0
        fields = ('question',)
        show_change_link = True

    list_display = ('id', 'name', 'card_color')
    search_fields = ('name',)
    inlines = [QuestionsInline]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    class AnswersInline(admin.TabularInline):
        model = QuizQuestionAnswer
        extra = 0

    list_display = ('id', 'quiz_batch', 'question')
    search_fields = ('question',)

    inlines = [AnswersInline]


@admin.register(UserQuizQuestion)
class UserQuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_tasks_profile',
                    'quiz_question', 'answer', 'coins_earned')


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    search_fields = ('question',)


@admin.register(UserSurveyAnswer)
class UserSurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_tasks_profile', 'survey_question', 'mark')
