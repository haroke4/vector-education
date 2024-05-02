from rest_framework import status
from rest_framework.response import Response


def error_with_text(text):
    return Response({'message': text}, status=status.HTTP_400_BAD_REQUEST)


def success_with_text(text):
    return Response({'message': text}, status=status.HTTP_200_OK)
