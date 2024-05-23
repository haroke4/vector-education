from protected_media.models import ProtectedImageField
from django.db import models
from .__component_base import ComponentBase


class MatchingComponent(ComponentBase):
    title = models.CharField(max_length=200, verbose_name='Заголовок', default='Соедините элементы')

    class Meta:
        verbose_name = 'Соедините элементы компонент'
        verbose_name_plural = 'Соедините элементы компоненты'

    def __str__(self):
        return f'{self.pk} MatchingComponent: "{self.title}"'


class MatchingComponentElementCouple(models.Model):
    component = models.ForeignKey(MatchingComponent, on_delete=models.CASCADE, related_name='element_couples',
                                  verbose_name='Компонент')
    first_element = models.OneToOneField('MatchingComponentElement', on_delete=models.CASCADE,
                                         related_name='first_element', verbose_name='Первый элемент')
    second_element = models.OneToOneField('MatchingComponentElement', on_delete=models.CASCADE,
                                          related_name='second_element', verbose_name='Второй элемент')

    class Meta:
        verbose_name = 'Пара элементов соединения'
        verbose_name_plural = 'Пары элементов соединения'

    def __str__(self):
        return f'{self.pk} MatchingComponentElementCouple: "{self.first_element.text}" - "{self.second_element.text}"'


class MatchingComponentElement(models.Model):
    text = models.CharField(max_length=200, verbose_name='Текст элемента')
    image = ProtectedImageField(upload_to='matching_elements/', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Элемент соединения'
        verbose_name_plural = 'Элементы соединения'

    def __str__(self):
        return f'{self.pk} MatchingComponentElement: "{self.text}"'

    def save(self, *args, **kwargs):
        if self.image:
            self.text = ''
        super().save(*args, **kwargs)
