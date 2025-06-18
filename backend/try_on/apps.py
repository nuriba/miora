from django.apps import AppConfig


class TryOnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'try_on'
    verbose_name = 'Virtual Try-On'