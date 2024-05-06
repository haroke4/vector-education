from rest_framework import serializers
from api_lessons.models import *
from backend.global_function import UserContextNeededSerializer


class LessonBatchSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = LessonBatch
        fields = '__all__'

    def get_lessons(self, obj):
        # returning only id's for security
        return [lesson.id for lesson in obj.lessons.all()]


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'


class QuestionSerializer(UserContextNeededSerializer, serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True)
    is_user_answered = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_is_user_answered(self, obj):
        return UserQuestionModel.objects.filter(user=self.user, question=obj).exists()


class LessonSerializer(UserContextNeededSerializer, serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_questions(self, obj):
        return QuestionSerializer(obj.questions.all(), many=True, user=self.user).data
