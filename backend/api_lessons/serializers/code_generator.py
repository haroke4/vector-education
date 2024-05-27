"""
Generates Serializers for all models in models/lesson_components
"""

from django.db import models

field_snippet = """
    {name} = {serializer_name}Serializer(many={many})
"""

snippet = """
class {model_name}Serializer(serializers.ModelSerializer):
    {serializer_fields}

    class Meta:
        model = {model_name}
        fields = '__all__'
"""


def get_fields_snippet(model, many, name):
    class_name = str(model).split('.')[-1][:-2]
    return field_snippet.format(serializer_name=class_name, many=many, name=name)


def get_serializer_snippet(model, fields):
    fields = [get_fields_snippet(*a) for a in fields]
    app_name = model._meta.app_label
    class_name = str(model).split('.')[-1][:-2]
    return snippet.format(model_name=class_name,
                          serializer_fields='\n\t'.join(fields))


def func():
    import importlib
    import os

    # Import and register each model
    models_dir = os.path.dirname(os.path.realpath(__file__)).replace('/serializers', '') + '/models/lesson_components/'
    model_files = [f for f in os.listdir(models_dir) if
                   os.path.isfile(os.path.join(models_dir, f)) and f.endswith('.py')]
    models_with_fields = {}
    just_models = []

    for model_file in model_files:
        module_name = model_file[:-3]  # Remove .py extension
        module = importlib.import_module(f'api_lessons.models.lesson_components.{module_name}')
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, models.Model):
                # if model is abstract, skip it
                if attr._meta.abstract:
                    continue
                if not getattr(attr, 'auto_gen_serializer', True):
                    continue
                just_model = True
                for field in attr._meta.fields:
                    if type(field) is models.ForeignKey:
                        host_model = field.related_model
                        name = field._related_name
                        models_with_fields[host_model] = models_with_fields.get(host_model, []) + [(attr, True, name)]

                    if type(field) is models.OneToOneField:
                        host_model = field.related_model
                        name = field.name
                        models_with_fields[attr] = models_with_fields.get(attr, []) + [(host_model, False, name)]

                if just_model:
                    just_models.append(attr)

    code_lines = []
    just_models = list(set(just_models))
    just_models = [i for i in just_models if i not in models_with_fields.keys()]
    for i in just_models:
        code_lines.append(get_serializer_snippet(i, []))

    sorted_keys = []

    def recursic_sort(model):
        for iter_model in models_with_fields.get(model, []):
            if iter_model[0] in just_models:
                continue
            # print(f'sending: {iter_model[0]} from {model}')
            recursic_sort(iter_model[0])
        if model in sorted_keys:
            return
        sorted_keys.append(model)

    for model in models_with_fields.keys():
        recursic_sort(model)

    for model in sorted_keys:
        fields = list(set(models_with_fields[model]))
        code_lines.append(get_serializer_snippet(model, fields))

    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    print('got_u')
    with open(this_file_dir + '/gen_components_serializers.py', 'w') as f:
        f.write('from api_lessons.models import *\n')
        f.write('from rest_framework import serializers\n\n#auto-generated\n\n')
        f.write(f"""{''.join(code_lines)[:-1]}""")


if __name__ == '__main__':
    func()
