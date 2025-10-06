from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        """
        This method is called when the app is ready.
        It's the recommended place to import and connect signals.
        """
        import messaging.signals