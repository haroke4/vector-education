from api_lessons.models import *
from rest_framework import serializers


# auto-generated


class FillTextLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillTextLine
        fields = '__all__'


class AudioComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioComponent
        fields = '__all__'


class RecordAudioComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordAudioComponent
        fields = '__all__'


class PutInOrderComponentElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutInOrderComponentElement
        fields = '__all__'


class MatchingComponentElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingComponentElement
        fields = '__all__'


class TextComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextComponent
        fields = '__all__'


class VideoComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComponent
        fields = '__all__'


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class BlueCardComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueCardComponent
        fields = '__all__'


class ImageComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageComponent
        fields = '__all__'


class MatchingComponentElementCoupleSerializer(serializers.ModelSerializer):
    first_element = MatchingComponentElementSerializer(many=False)

    second_element = MatchingComponentElementSerializer(many=False)

    class Meta:
        model = MatchingComponentElementCouple
        fields = '__all__'


class MatchingComponentSerializer(serializers.ModelSerializer):
    element_couples = MatchingComponentElementCoupleSerializer(many=True)

    class Meta:
        model = MatchingComponent
        fields = '__all__'


class FillTextComponentSerializer(serializers.ModelSerializer):
    lines = FillTextLineSerializer(many=True)

    class Meta:
        model = FillTextComponent
        fields = '__all__'


class PutInOrderComponentSerializer(serializers.ModelSerializer):
    elements = PutInOrderComponentElementSerializer(many=True)

    class Meta:
        model = PutInOrderComponent
        fields = '__all__'


class QuestionComponentSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = QuestionComponent
        fields = '__all__'


class LessonPageElementSerializer(serializers.ModelSerializer):
    blue_card_component = BlueCardComponentSerializer(many=False)

    audio_component = AudioComponentSerializer(many=False)

    matching_component = MatchingComponentSerializer(many=False)

    record_audio_component = RecordAudioComponentSerializer(many=False)

    video_component = VideoComponentSerializer(many=False)

    put_in_order_component = PutInOrderComponentSerializer(many=False)

    text_component = TextComponentSerializer(many=False)

    fill_text_component = FillTextComponentSerializer(many=False)

    question_component = QuestionComponentSerializer(many=False)

    image_component = ImageComponentSerializer(many=False)

    class Meta:
        model = LessonPageElement
        fields = '__all__'


class LessonPageSerializer(serializers.ModelSerializer):
    elements = LessonPageElementSerializer(many=True)

    class Meta:
        model = LessonPage
        fields = '__all__'
