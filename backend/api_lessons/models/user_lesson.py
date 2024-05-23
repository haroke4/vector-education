from decimal import Decimal

from django.db import models
from api_users.models import UserModel
from api_lessons.models import Lesson
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class UserLessonModel(models.Model):
    user = models.ForeignKey('api_users.UserModel', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='lessons')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, verbose_name='Урок')
    completed = models.BooleanField(default=False, verbose_name='Урок завершен')


# class UserQuestionModel(models.Model):
#     user = models.ForeignKey('api_users.UserModel', on_delete=models.CASCADE, verbose_name='Пользователь')
#     question = models.ForeignKey('QuestionComponent', on_delete=models.CASCADE, verbose_name='Вопрос')
#
#     def __str__(self):
#         return f'{self.pk} UserQuestionModel'
#
#     class Meta:
#         verbose_name = 'Ответ пользователя на вопрос урока'
#         verbose_name_plural = 'Ответы пользователя на вопросы урока'
