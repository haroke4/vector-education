from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.request import Request

from api_users.serializers import *
from api_users.models import *
from api_users.serializers.model_serializers import UserModelSerializer
from backend.global_function import success_with_text


class SetCloudMessagingToken(APIView):
    permission_classes = []

    def post(self, request: Request, *args, **kwargs):
        pass


class GetUserView(APIView):
    def get(self, request: Request):
        user: UserModel = request.user
        user.update_activity_date(register_login=True)
        user.last_login_datetime = timezone.now()
        return success_with_text(UserModelSerializer(user).data)


class UpdateDayStreak(APIView):
    def post(self, request: Request):
        user: UserModel = request.user
        user.update_activity_date(register_login=False)
        return success_with_text(UserModelSerializer(user).data)
