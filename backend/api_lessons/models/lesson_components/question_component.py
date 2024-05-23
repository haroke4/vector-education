from protected_media.models import ProtectedImageField
from django.db import models
from .__component_base import ComponentBase


class QuestionComponent(ComponentBase):
    text = models.CharField(max_length=2000, verbose_name='Текст вопроса')

    class Meta:
        verbose_name = 'Вопрос компонент'
        verbose_name_plural = 'Вопросы компоненты'
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
