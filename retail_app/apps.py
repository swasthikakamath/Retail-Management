from django.apps import AppConfig


class RetailAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'retail_app'
    def ready(self):
        import retail_app.signals
