import os
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured


class ApiBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_base'

    def ready(self):
        super().ready()

        if not os.path.exists('service_account.json'):
            raise ImproperlyConfigured('service_account.json file is missing')

        import firebase_admin
        from firebase_admin import credentials

        cred = credentials.Certificate("service_account.json")
        firebase_admin.initialize_app(cred)
        print("Firebase admin is initialized")
