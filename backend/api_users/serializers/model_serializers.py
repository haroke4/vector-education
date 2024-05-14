from rest_framework import serializers

from api_users.models import UserModel, UserTypes
from api_lessons.models import Lesson, UserLessonModel

class UserModelSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    paid = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        # excluding default django user fields
        exclude = ['password', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups',
                   'user_permissions', 'first_name', 'last_name', 'photo_url', 'firebase_user_id', 'fcm_token',
                   'user_type']

    def get_photo(self, obj: UserModel):
        if obj.photo:
            return obj.photo.url
        return obj.photo_url

    def get_paid(self, obj: UserModel):
        return not (obj.user_type == UserTypes.free)

    def get_progress(self, obj: UserModel):
        all_lessons = Lesson.objects.all().count()
        user_lessons = UserLessonModel.objects.filter(user=obj, completed=True).count()
        if all_lessons == 0:
            return 1
        return user_lessons / all_lessons

