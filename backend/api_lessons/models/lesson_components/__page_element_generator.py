from .__component_base import ComponentBase

"""
Run this file in order to automatically create fields with components.
"""


def page_element_generator():
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
                    f'''{model_name} = models.OneToOneField('{app_name}.{class_name}', on_delete=models.CASCADE, related_name='page_element', blank=True, null=True)\n''')
                added_models.append(attr)

    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(this_file_dir, '__page_element.py')
    with open(script_path, 'r') as f:
        this_script = list(f)
        index = this_script.index('    # components:  :3\n')
        this_script = this_script[:index + 1]

    with open(script_path, 'w') as f:
        f.write(f'''{''.join(this_script)[:-1]}\n    {'    '.join(code_lines)}\n''')


if __name__ == '__main__':
    page_element_generator()
