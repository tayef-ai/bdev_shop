from django.apps import AppConfig


class EcomappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecomapp'
    def ready(self):
        import ecomapp.signals