from rest_framework.views import APIView
from rest_framework.request import Request

from api_users.serializers import *
from backend.global_function import error_with_text, success_with_text


class EditNameOrDescriptionView(APIView):
    def post(self, request: Request):
        serializer = EditNameOrDescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: UserModel = request.user
        user.name = serializer.validated_data.get('name', user.name)
        user.description = serializer.validated_data.get('description', user.description)
        user.save()

        return success_with_text(UserModelSerializer(user).data)


class EditPhotoView(APIView):
    def post(self, request: Request):
        data = request.data.dict()
        if data.get('image', None) is not None:
            if request.user.photo:
                request.user.photo.delete()

            image_data = data.pop('image')
            request.user.photo = image_data
            request.user.save()

            return success_with_text(UserModelSerializer(request.user).data)
        return error_with_text('No image provided')
