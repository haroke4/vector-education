from django.db import models
from api_users.models import UserModel


class LessonBatchNames:
    @staticmethod
    def choices():
        return (
            ('listening', 'Listening'),
            ('speaking', 'Speaking'),
            ('reading', 'Reading'),
            ('writing', 'Writing'),
            ('addition', 'Additional'),
        )


class LessonBatch(models.Model):
    title = models.CharField(max_length=255, choices=LessonBatchNames.choices(),
                             verbose_name='Название коллекции уроков')

    def __str__(self):
        return f'{self.pk} Lesson Batch: "{self.title}"'

    class Meta:
        verbose_name = 'Коллекция уроков'
        verbose_name_plural = 'Коллекции уроков'


class Lesson(models.Model):
    is_available_on_free = models.BooleanField(default=False, verbose_name='Доступен на бесплатном тарифе')
    lesson_batch = models.ForeignKey(LessonBatch, on_delete=models.CASCADE, verbose_name='Коллекция уроков',
                                     related_name='lessons')
    topic = models.CharField(max_length=200, verbose_name='Тема')
    description = models.CharField(max_length=2000, verbose_name='Описание')
    video_url = models.URLField(verbose_name='Ссылка на видео')

    def __str__(self):
        return f'{self.pk} Lesson: {self.topic} '

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', related_name='questions')
    text = models.CharField(max_length=2000, verbose_name='Текст вопроса')

    def __str__(self):
        return f'{self.pk} Question: "{self.text}"'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='answers')
    text = models.CharField(max_length=2000, verbose_name='Ответ')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return f'{self.pk} QuestionAnswer: "{self.text}"'

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'
