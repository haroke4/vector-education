from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework import serializers

from api_users.models import UserModel


def error_with_text(text):
    return Response({'message': text}, status=status.HTTP_400_BAD_REQUEST)


def success_with_text(text):
    return Response({'message': text}, status=status.HTTP_200_OK)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        return error_with_text(exc.detail)

    return response


class UserContextNeededSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if isinstance(user, UserModel):
            if not user.is_authenticated:
                raise Exception('User must be authenticated')
            self.user = user
        else:
            raise Exception('User context needed')
