from django.db.models import Sum
from rest_framework.request import Request
from rest_framework.views import APIView

from backend.response import success_with_text, error_with_text
from .serializers import *
from .model_serializers import *
from .models import *


class GetQuizzesView(APIView):
    def get(self, request: Request):
        quizzes = QuizBatch.objects.all()
        return success_with_text(QuizBatchSerializer(quizzes, many=True).data)


class GetQuizQuestionView(APIView):
    def post(self, request: Request):
        serializer = GetQuizQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return error_with_text(serializer.errors)

        quiz: QuizBatch = serializer.validated_data['quiz_id']  # type: ignore
        user_tasks_profile: UserTasksProfile = request.user.user_profile.tasks_profile

        completed_quiz_questions = UserQuizQuestion.objects.filter(
            user_tasks_profile=user_tasks_profile,
            quiz_question__quiz_batch=quiz,
            answer__isnull=False
        ).values_list('quiz_question', flat=True).distinct().all()
        not_completed_quiz_questions = quiz.questions.exclude(
            id__in=completed_quiz_questions)
        question = not_completed_quiz_questions.first()

        if question is None:
            if not user_tasks_profile.completed_quizzes.filter(id=quiz.id).exists():
                # за прохождение викторины даем 10 монет
                user_tasks_profile.completed_quizzes.add(quiz)
                user_tasks_profile.add_coins(10)
            all_earned_coins_from_quiz = UserQuizQuestion.objects.filter(
                user_tasks_profile=user_tasks_profile,
                quiz_question__quiz_batch=quiz
            ).aggregate(Sum('coins_earned'))['coins_earned__sum']
            return success_with_text({
                'questions_left': 0,
                'total_coins': all_earned_coins_from_quiz,
            })

        question_data = QuizQuestionSerializer(question).data
        questions_left = not_completed_quiz_questions.count()
        return success_with_text(
            {
                'questions_left': questions_left,
                'all_question_count': quiz.questions.count(),
                'question_data': question_data,
            }
        )


class AnswerToQuizQuestionView(APIView):

    def post(self, request: Request):
        serializer = AnswerToQuizQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return error_with_text(serializer.errors)

        answer: QuizQuestionAnswer = serializer.validated_data['answer_id']
        user_tasks_profile: UserTasksProfile = request.user.user_profile.tasks_profile
        question: QuizQuestion = answer.quiz_question

        a = UserQuizQuestion.objects.filter(
            user_tasks_profile=user_tasks_profile, quiz_question=question).first()
        if a is not None:
            return error_with_text('already_answered')

        correct_answer_id = -1
        coins = 0
        if answer.is_correct:
            coins = user_tasks_profile.correct_answer()
            correct_answer_id = answer.id
        else:
            user_tasks_profile.incorrect_answer()
            a = question.answers.filter(is_correct=True).first()
            if a is not None:
                correct_answer_id = a.id
        UserQuizQuestion.objects.create(user_tasks_profile=user_tasks_profile, quiz_question=question, answer=answer,
                                        coins_earned=coins)

        return success_with_text({'correct_answer_id': correct_answer_id, 'coins': coins})


# ---------------------- Surveys ----------------------
class GetSurveyQuestion(APIView):
    def get(self, request: Request):
        user_tasks_profile: UserTasksProfile = request.user.user_profile.tasks_profile
        question = SurveyQuestion.objects.exclude(
            answers__user_tasks_profile=user_tasks_profile).first()
        if question is None:
            if not user_tasks_profile.survey_completed:
                user_tasks_profile.survey_completed = True
                user_tasks_profile.user_profile.add_xp_and_coins(coins=10)
            return success_with_text('no_questions')
        return success_with_text(SurveyQuestionSerializer(question).data)


class AnswerToSurveyQuestion(APIView):
    def post(self, request: Request):
        serializer = AnswerToSurveyQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return error_with_text(serializer.errors)

        question: SurveyQuestion = serializer.validated_data['survey_id']
        user_tasks_profile: UserTasksProfile = request.user.user_profile.tasks_profile

        if question.answers.filter(user_tasks_profile=user_tasks_profile).count() != 0:
            return error_with_text('already_answered')

        UserSurveyAnswer.objects.create(user_tasks_profile=user_tasks_profile,
                                        survey_question=question,
                                        mark=serializer.validated_data['mark'])
        return success_with_text('ok')
