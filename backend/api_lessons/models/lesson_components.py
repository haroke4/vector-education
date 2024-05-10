from django.db import models
from api_users.models import UserModel
from .lesson import Lesson


class ConspectusComponent(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок', default='Конспект')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Конспект'
        verbose_name_plural = 'Конспекты'

    def __str__(self):
        return f'{self.pk} ConspectusComponent: "{self.title}"'


class VideoComponent(models.Model):
    description = models.CharField(max_length=2000, verbose_name='Описание')
    video_url = models.URLField(verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'Видео компонент'
        verbose_name_plural = 'Видео компоненты'

    def __str__(self):
        return f'{self.pk} VideoComponent: "{self.description}"'


class QuestionComponent(models.Model):
    text = models.CharField(max_length=2000, verbose_name='Текст вопроса')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']

    def __str__(self):
        return f'{self.pk} QuestionComponent: "{self.text}"'


class QuestionAnswer(models.Model):
    question = models.ForeignKey(QuestionComponent, on_delete=models.CASCADE, verbose_name='Вопрос',
                                 related_name='answers')
    text = models.CharField(max_length=2000, verbose_name='Ответ')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return f'{self.pk} QuestionAnswer: "{self.text}"'

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'


class LessonComponentTypes:
    video = 'video'
    question = 'question'
    conspectus = 'conspectus'

    @staticmethod
    def choices():
        return (
            (LessonComponentTypes.video, 'Видео'),
            (LessonComponentTypes.question, 'Вопрос'),
            (LessonComponentTypes.conspectus, 'Конспект'),
        )


class LessonComponent(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', related_name='components')
    type = models.CharField(max_length=20, choices=LessonComponentTypes.choices(), verbose_name='Тип компонента')
    order = models.PositiveIntegerField(verbose_name='Порядок')

    # actual components
    video_component = models.OneToOneField(VideoComponent, on_delete=models.CASCADE, null=True, blank=True)
    question_component = models.OneToOneField(QuestionComponent, on_delete=models.CASCADE, null=True, blank=True)
    conspectus_component = models.OneToOneField(ConspectusComponent, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Компонент урока'
        verbose_name_plural = 'Компоненты уроков'
        ordering = ['order']

    def __str__(self):
        return f'{self.pk} LessonComponent: {self.type}'

    def save(self, *args, **kwargs):
        if self.type == LessonComponentTypes.video:
            if not self.video_component:
                raise ValueError("Video component is not set")
        elif self.type == LessonComponentTypes.question:
            if not self.question_component:
                raise ValueError("Question component is not set")
        elif self.type == LessonComponentTypes.conspectus:
            if not self.conspectus_component:
                raise ValueError("Conspectus component is not set")
        else:
            raise ValueError("Unknown component type")

        super().save(*args, **kwargs)
