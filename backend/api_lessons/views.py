from rest_framework.views import APIView

from backend.response import success_with_text
from .models import Lesson, AdditionalMaterial
from .serializers import *


class GetLessons(APIView):
    def get(self, request, category):
        data = Lesson.objects.filter(category=category)
        return success_with_text(LessonSerializer(data, many=True))


class GetAdditionalMaterials(APIView):
    def get(self, request):
        data = AdditionalMaterial.objects.all()
        return success_with_text(AdditionalMaterialSerializer(data, many=True))
