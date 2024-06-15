from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.request import Request

from api_users.serializers import *
from api_users.models import *
from api_users.serializers.model_serializers import UserModelSerializer
from backend.global_function import success_with_text, error_with_text


class SetFCMToken(APIView):
    def post(self, request: Request, *args, **kwargs):
        user: UserModel = request.user
        token = request.data.get('token', None)
        if token is None:
            return error_with_text('Token is required')
        user.fcm_token = token
        user.save()
        return success_with_text('Token set')


class GetUserView(APIView):
    def get(self, request: Request):
        user: UserModel = request.user
        user.last_login = timezone.now()
        user.save()

        # Проверка на дневную серию (если пропущено то обновляем)
        last_active_date = user.activity_dates.last()
        if last_active_date is not None:
            difference = (timezone.now().date() - last_active_date.datetime.date()).seconds
            if difference > 48 * 3600:
                user.day_streak = 0
                user.save()

        user.last_login_datetime = timezone.now()
        return success_with_text(UserModelSerializer(user).data)


class UpdateDayStreak(APIView):
    def post(self, request: Request):
        user: UserModel = request.user

        today = timezone.now()
        last_active_date = user.activity_dates.first()

        # Если пользователь никогда не заходил, то ставим вчерашнюю дату
        if last_active_date is None:
            last_active_date = (timezone.now() - timezone.timedelta(days=1)).date()
        else:
            last_active_date = last_active_date.datetime.date()

        # Некая фильтрация
        # Если прошло меньше 5ти минут с последнего входа, то не обновляем активность
        last_login_difference = (today - user.last_login).seconds
        if last_login_difference < 300:
            return error_with_text('Too early to update activity date')
        elif last_login_difference > 1000:
            return error_with_text('Too late to update activity date, login again')

        # Логика самого day streak
        difference = (today.date() - last_active_date).hours
        if difference < 24:
            return error_with_text('Already updated today')

        user.day_streak += 1
        if user.day_streak > user.max_day_streak:
            user.max_day_streak = user.day_streak
        user.save()
        user.add_points(points=1, description='Бонус за дневную серию')

        # Если у пользователя 10 дней подряд, то даем ему 5 бонусных баллов
        if user.day_streak % 10 == 0:
            user.add_points(points=5, description='Бонусы за 10 дней подряд')

        # Создаем новую активность
        user.activity_dates.create()

        return success_with_text(UserModelSerializer(user).data)
