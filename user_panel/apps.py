from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'user_panel'

    def ready(self):
        from user_panel import signals
