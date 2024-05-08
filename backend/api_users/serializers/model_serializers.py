from rest_framework import serializers

from api_users.models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        # excluding default django user fields
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups',
                   'user_permissions', 'first_name', 'last_name', 'photo_url', 'firebase_user_id', 'fcm_token']

    def get_photo(self, obj: UserModel):
        if obj.photo:

            return obj.photo.url
        return obj.photo_url

