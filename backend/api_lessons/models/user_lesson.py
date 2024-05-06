from django.db import models
from api_users.models import UserModel
from api_lessons.models import Lesson


class UserQuestionModel(models.Model):
    user = models.ForeignKey('api_users.UserModel', on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос')

    def __str__(self):
        return f'{self.pk} UserQuestionModel'

    class Meta:
        verbose_name = 'Ответ пользователя на вопрос урока'
        verbose_name_plural = 'Ответы пользователя на вопросы урока'
