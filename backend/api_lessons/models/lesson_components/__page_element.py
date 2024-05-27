from django.db import models
from rest_framework.exceptions import ValidationError

from .__component_base import LessonPage, ComponentBase

"""
Run this file in order to automatically create fields with components.
"""


def func():
    import importlib
    import os

    # Get the directory of the models
    models_dir = os.path.dirname(os.path.realpath(__file__))

    # Get all python files in the directory
    model_files = [f for f in os.listdir(models_dir) if
                   os.path.isfile(os.path.join(models_dir, f)) and f.endswith('.py')]
    code_lines = []
    added_models = []

    # Import and register each model
    for model_file in model_files:
        module_name = model_file[:-3]
        module = importlib.import_module(f'api_lessons.models.lesson_components.{module_name}')
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, ComponentBase):
                # if model is abstract, skip it
                if attr._meta.abstract:
                    continue
                if attr in added_models:
                    continue
                class_name = str(attr).split('.')[-1][:-2]

                # model_name = class name from camel case to snake case
                model_name = ''.join(['_' + i.lower() if i.isupper() else i for i in class_name]).lstrip('_')

                app_name = attr._meta.app_label
                code_lines.append(
                    f'''{model_name} = models.OneToOneField('{app_name}.{class_name}', on_delete=models.CASCADE, related_name='page_element', blank=True, null=True)''')
                added_models.append(attr)

    with open(__file__, 'r') as f:
        this_script = list(f)
        index = this_script.index('    # components:  :3\n')
        this_script = this_script[:index + 1]

    with open(__file__, 'w') as f:
        f.write(f'''{''.join(this_script)[:-1]}
    {'\n\t'.join(code_lines)}
    ''')


if __name__ == '__main__':
    func()


class LessonPageElement(models.Model):
    class Meta:
        verbose_name = 'Элемент страницы урока'
        verbose_name_plural = 'Элементы страницы урока'
        ordering = ['order']

    def __str__(self):
        return f'{self.pk} LessonPageElement'

    def save(self, *args, **kwargs):
        if self.page.elements.filter(order=self.order).exclude(pk=self.pk).exists():
            raise ValidationError('Order must be unique in page')

        super().save(*args, **kwargs)

    page = models.ForeignKey(LessonPage, on_delete=models.CASCADE, related_name='elements', verbose_name='Страница')
    order = models.PositiveIntegerField(verbose_name='Порядок элемента на странице')

    # components:  :3
    matching_component = models.OneToOneField('api_lessons.MatchingComponent', on_delete=models.CASCADE,
                                              related_name='page_element', blank=True, null=True)
    audio_component = models.OneToOneField('api_lessons.AudioComponent', on_delete=models.CASCADE,
                                           related_name='page_element', blank=True, null=True)
    blue_card_component = models.OneToOneField('api_lessons.BlueCardComponent', on_delete=models.CASCADE,
                                               related_name='page_element', blank=True, null=True)
    fill_text_component = models.OneToOneField('api_lessons.FillTextComponent', on_delete=models.CASCADE,
                                               related_name='page_element', blank=True, null=True)
    image_component = models.OneToOneField('api_lessons.ImageComponent', on_delete=models.CASCADE,
                                           related_name='page_element', blank=True, null=True)
    put_in_order_component = models.OneToOneField('api_lessons.PutInOrderComponent', on_delete=models.CASCADE,
                                                  related_name='page_element', blank=True, null=True)
    question_component = models.OneToOneField('api_lessons.QuestionComponent', on_delete=models.CASCADE,
                                              related_name='page_element', blank=True, null=True)
    record_audio_component = models.OneToOneField('api_lessons.RecordAudioComponent', on_delete=models.CASCADE,
                                                  related_name='page_element', blank=True, null=True)
    text_component = models.OneToOneField('api_lessons.TextComponent', on_delete=models.CASCADE,
                                          related_name='page_element', blank=True, null=True)
    video_component = models.OneToOneField('api_lessons.VideoComponent', on_delete=models.CASCADE,
                                           related_name='page_element', blank=True, null=True)
