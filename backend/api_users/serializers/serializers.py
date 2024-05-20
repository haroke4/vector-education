from rest_framework import serializers

from api_users.models import UserModel


class FireBaseAuthSerializer(serializers.Serializer):
    token = serializers.CharField()


class EditNameOrDescriptionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, min_length=2)
    description = serializers.CharField(max_length=80, min_length=2)


class SearchUserSerializer(serializers.Serializer):
    search = serializers.CharField(max_length=50, min_length=1)


class GetUserByIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, obj):
        try:
            user = UserModel.objects.get(id=obj)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('User with this id ID does not exist')
        return user
