from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"

    def ready(self):
        from .signals import initialize_groups
        post_migrate.connect(initialize_groups, sender=self)