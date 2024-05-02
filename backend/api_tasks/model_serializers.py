from rest_framework import serializers
from .models import *


class QuizQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestionAnswer
        exclude = ('quiz_question', 'is_correct')


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizQuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        exclude = []


class QuizBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizBatch
        exclude = []


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        exclude = []
