from rest_framework import serializers


class FireBaseAuthSerializer(serializers.Serializer):
    token = serializers.CharField()


class EditNameOrDescriptionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=80)