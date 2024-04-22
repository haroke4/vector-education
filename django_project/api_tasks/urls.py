from django.urls import path
from .views import *

urlpatterns = [
    path('get_quizzes/', GetQuizzesView.as_view()),
    path('get_quiz_question/', GetQuizQuestionView.as_view()),
    path('answer_to_quiz_question/', AnswerToQuizQuestionView.as_view()),

    path('get_survey_question/', GetSurveyQuestion.as_view()),
    path('answer_to_survey_question/', AnswerToSurveyQuestion.as_view()),
]
