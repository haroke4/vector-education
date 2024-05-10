from rest_framework import serializers
from api_lessons.models import *


class AnswerToQuestionSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()

    def validate_answer_id(self, answer_id):
        try:
            answer = QuestionAnswer.objects.get(id=answer_id)
        except QuestionAnswer.DoesNotExist:
            raise serializers.ValidationError('Answer does not exist')
        return answer
