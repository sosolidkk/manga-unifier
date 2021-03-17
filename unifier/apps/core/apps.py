from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "unifier.apps.core"

    def ready(self):
        import unifier.apps.core.signals
