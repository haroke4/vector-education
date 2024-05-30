from rest_framework.request import Request
from rest_framework.views import APIView
from api_lessons.models import *
from api_lessons.serializers import *
from api_lessons.serializers import *
from backend.global_function import *


class AnswerFillTextComponentView(APIView):
    def post(self, request: Request):
        serializer = AnswerToFillTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        for item in serializer.validated_data['lines']:
            line: FillTextLine = item['line_id']
            answer: str = item['answer']
            lesson = line.component.get_lesson()

            if lesson is None:
                return error_with_text('this lesson is deprecated')

            if not lesson.is_available_for_user(user):
                return error_with_text('Lesson is not available for user')

            UserFillTextAnswer.objects.create(user=user, line=line, answer=answer)

        return success_with_text('Answers added')


class AnswerMatchingComponentView(APIView):
    def post(self, request: Request):
        serializer = AnswerToMatchingComponentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        first_element = serializer.validated_data['first_element_id']
        second_element = serializer.validated_data['second_element_id']
        couple = second_element.second_element
        lesson = couple.component.get_lesson()

        if lesson is None:
            return error_with_text('this lesson is deprecated')

        if not lesson.is_available_for_user(user):
            return error_with_text('Lesson is not available for user')

        UserMatchingComponentElementCouple.objects.create(user=user, couple=couple, first_element=first_element,
                                                          second_element=second_element)

        return success_with_text('Answer added')


class AnswerPutInOrderComponentView(APIView):
    def post(self, request: Request):
        serializer = AnswerToPutInOrderComponentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        elements = serializer.validated_data
        lesson = elements[0].element.component.get_lesson()

        if lesson is None:
            return error_with_text('this lesson is deprecated')

        if not lesson.is_available_for_user(user):
            return error_with_text('Lesson is not available for user')

        for element in elements:
            UserPutInOrderAnswer.objects.create(user=user, element=element['element_id'], order=element['order'])

        return success_with_text('Answer added')


class AnswerQuestionComponentView(APIView):
    def post(self, request: Request):
        serializer = AnswerToQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        answer: QuestionAnswer = serializer.validated_data['answer_id']
        lesson = answer.question.get_lesson()

        if lesson is None:
            return error_with_text('this lesson is deprecated')

        if not lesson.is_available_for_user(user):
            return error_with_text('Lesson is not available for user')

        UserQuestionAnswer.objects.create(user=user, answer=answer)

        return success_with_text('Answer added')


class AnswerRecordAudioComponentView(APIView):
    def post(self, request: Request):
        data = request.data.dict()
        user = request.user
        component = data.get('component_id', None)
        if component is None:
            return error_with_text('No component id provided')
        file = data.get('file', None)
        if file is None:
            return error_with_text('No file provided')

        component: RecordAudioComponent = RecordAudioComponent.objects.filter(id=component).first()
        if component is None:
            return error_with_text('Component does not exist')
        lesson = component.get_lesson()
        if lesson is None:
            return error_with_text('Lesson is deprecated')

        if not lesson.is_available_for_user(user):
            return error_with_text('Lesson is not available for user')

        previous_ans = UserRecordAudioComponent.objects.filter(user=user, component=component).first()
        if previous_ans:
            previous_ans.file.delete()
            previous_ans.delete()

        UserRecordAudioComponent.objects.create(user=user, component=component, file=file)
        return success_with_text('Answer added')
