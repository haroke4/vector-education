from django.urls import path
from .views import *

urlpatterns = [
    path('get_lesson_batch/', GetLessonsBatchView.as_view()),
    path('get_lesson/', GetLessonView.as_view()),
    path('answer_to_question/', AnswerToQuestionView.as_view()),
]
