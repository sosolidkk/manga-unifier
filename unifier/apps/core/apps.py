from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "unifier.apps.core"

    def ready(self):
        from unifier.apps.core.signals import create_auth_token
