from django.db import models
from .__component_base import ComponentBase


class PutInOrderComponent(ComponentBase):
    title = models.CharField(max_length=200, verbose_name='Заголовок', default='Поставьте в правильном порядке')

    class Meta:
        verbose_name = 'Поставьте в правильном порядке компонент'
        verbose_name_plural = 'Поставьте в правильном порядке компоненты'

    def __str__(self):
        return f'{self.pk} PutInOrderComponent: "{self.title}"'


class PutInOrderComponentElement(models.Model):
    component = models.ForeignKey(PutInOrderComponent, on_delete=models.CASCADE, related_name='elements',
                                  verbose_name='Компонент')
    text = models.CharField(max_length=200, verbose_name='Текст элемента')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Элемент компонента поставьте в правильном порядке'
        verbose_name_plural = 'Элементы компонента поставьте в правильном порядке'

    def save(self, *args, **kwargs):
        query = self.component.elements.filter(order=self.order)
        if self.pk:
            query = query.exclude(pk=self.pk)
        if query.exists():
            raise ValueError('Order must be unique in component')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk} PutInOrderComponentElement: "{self.text}"'
