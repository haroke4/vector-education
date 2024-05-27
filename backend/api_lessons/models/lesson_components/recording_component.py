from django.db import models
from .__component_base import ComponentBase


class RecordAudioComponent(ComponentBase):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Запись аудио компонент'
        verbose_name_plural = 'Запись аудио компоненты'

    def __str__(self):
        return f'{self.pk} RecordAudioComponent '


class UserRecordAudioComponent(models.Model):
    auto_gen_serializer = False
    component = models.ForeignKey(RecordAudioComponent, on_delete=models.CASCADE, verbose_name='Компонент',
                                  related_name='user_records')
    file = models.FileField(upload_to='audio/', verbose_name='Аудио файл')
    teacher_comment = models.TextField(verbose_name='Комментарий учителя', blank=True, null=True)

    class Meta:
        verbose_name = 'Записи пользователей аудио компонент'
        verbose_name_plural = 'Записи пользователей аудио компоненты'

    def __str__(self):
        return f'{self.pk} UserRecordAudioComponent: "{self.title}"'
