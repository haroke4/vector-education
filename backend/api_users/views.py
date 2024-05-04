from django.db import IntegrityError
from firebase_admin import auth
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView

from .models import UserModel
from api_users.serializers.serializers import FireBaseAuthSerializer
from backend.response import error_with_text, success_with_text
from .serializers.model_serializers import UserModelSerializer


class AuthViaFirebase(APIView):
    serializer_class = FireBaseAuthSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_with_text(serializer.errors)
        token = serializer.validated_data['token']

        # trying  to decode token, if not valid return error
        try:
            decoded_token = auth.verify_id_token(token)
        except ValueError:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        # trying to get the user id from the token, if not valid return error
        try:
            firebase_user_id = decoded_token['uid']
        except KeyError:
            return error_with_text('The user provided with the auth token is not a valid '
                                   'Firebase user, it has no Firebase UID')

        # trying to get the user from the database, if not found create a new user
        try:
            user_profile = UserModel.objects.get(firebase_user_id=firebase_user_id)
        except UserModel.DoesNotExist:
            firebase_user = auth.get_user(firebase_user_id)
            try:
                user_profile = UserModel.objects.create(
                    name=firebase_user.display_name,
                    email=firebase_user.email,
                    firebase_user_id=firebase_user_id
                )
            except IntegrityError:
                return error_with_text('A user with the provided Firebase UID already exists')

        # delete old token and generate a new one
        Token.objects.filter(user=user_profile).delete()
        token = Token.objects.create(user=user_profile)
        return success_with_text(UserModelSerializer(user_profile).data | {'token': token.key})

class SetCloudMessagingToken(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        pass



@api_view(["GET"])
def get_welcome_info(request):
    return success_with_text({"id": 1, "name": "Alibi", "days_straight": 365, "progress": 99})
