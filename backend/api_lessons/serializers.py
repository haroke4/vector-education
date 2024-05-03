from rest_framework import serializers
from .models import Lesson, AdditionalMaterial


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class AdditionalMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalMaterial
        fields = '__all__'
