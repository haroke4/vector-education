from rest_framework import serializers
from .models import *


class GetQuizQuestionSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()

    def validate_quiz_id(self, value):
        try:
            quiz = QuizBatch.objects.get(id=value)
        except QuizBatch.DoesNotExist:
            raise serializers.ValidationError('Викторина не найдена')
        return quiz


class AnswerToQuizQuestionSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()

    def validate_answer_id(self, value):
        try:
            answer = QuizQuestionAnswer.objects.get(id=value)
        except QuizQuestionAnswer.DoesNotExist:
            raise serializers.ValidationError('Ответ не найден')
        return answer


class AnswerToSurveyQuestionSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField()
    mark = serializers.IntegerField(min_value=1, max_value=10)

    def validate_survey_id(self, value):
        try:
            question = SurveyQuestion.objects.get(id=value)
        except UserSurveyAnswer.DoesNotExist:
            raise serializers.ValidationError('Ответ не найден')
        return question
