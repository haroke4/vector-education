from rest_framework.views import APIView
from api_lessons.models import *
from api_lessons.serializers import *
from api_lessons.serializers import *
from backend.global_function import *


class GetLessonsBatchView(APIView):
    def get(self, request):
        lessons_batch = LessonBatch.objects.all()
        return success_with_text(LessonBatchSerializer(lessons_batch, user=request.user, many=True).data)


class GetLessonView(APIView):
    def post(self, request):
        serializer = GetLessonById(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson: Lesson = serializer.validated_data['lesson_id']
        user: UserModel = request.user
        if not user.is_paid() and not lesson.is_available_on_free:
            return error_with_text('lesson_not_available')

        return success_with_text(LessonSerializer(lesson, user=request.user).data)


class AnswerToQuestionView(APIView):
    def post(self, request):
        serializer = AnswerToQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer: QuestionAnswer = serializer.validated_data['answer_id']
        user: UserModel = request.user

        if not user.is_paid() and not answer.question.lesson.is_available_on_free:
            return error_with_text('lesson_not_available')
        if answer.is_correct:
            UserQuestionModel.objects.get_or_create(user=user, question=answer.question)
        return success_with_text({'is_correct': answer.is_correct})
