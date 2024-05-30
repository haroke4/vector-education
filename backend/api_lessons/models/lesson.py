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
    title = models.CharField(max_length=200, verbose_name='Тема')
    order = models.IntegerField(verbose_name='Порядок урока в коллекции')

    def __str__(self):
        return f'{self.pk} Lesson: {self.title} '

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']

    def is_available_for_user(self, user: UserModel) -> bool:
        return self.is_available_on_free or user.is_paid()
