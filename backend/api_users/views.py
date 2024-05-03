from django.db import IntegrityError
from firebase_admin import auth
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view

from backend.response import success_with_text
from .models import UserProfile
from .serializers import FireBaseAuthSerializer


class FireBaseAuthAPI(generics.GenericAPIView):
    serializer_class = FireBaseAuthSerializer

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            decoded_token = auth.verify_id_token(token)
        except ValueError:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            firebase_user_id = decoded_token['uid']
        except KeyError:
            return Response({'detail': 'The user provided with the auth token is not a valid Firebase user, it has no Firebase UID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(
                firebase_user_id=firebase_user_id)
            content = {
                "username": user.username,
                "email": user.email,
                "firebase_user_id": user.firebase_user_id
            }
            return Response(content, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            user = auth.get_user(firebase_user_id)
            try:
                new_user = UserProfile.objects.create(
                    username=user.display_name,
                    email=user.email,
                    firebase_user_id=firebase_user_id
                )
                content = {
                    "username": new_user.username,
                    "email": new_user.email,
                    "firebase_user_id": new_user.firebase_user_id
                }
                return Response(content, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'detail': 'A user with the provided Firebase UID already exists'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_welcome_info(request):
    return success_with_text({"id": 1, "name": "Alibi", "days_straight": 365, "progress": 99})
