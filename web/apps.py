from django.apps import AppConfig


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'

    def ready(self):
        """Запуск планировщиков при старте приложения."""
        from web.updater import updater
        updater.start()
        from web.notifier import notifier
        notifier.start()
