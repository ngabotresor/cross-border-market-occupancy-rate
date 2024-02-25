from django.apps import AppConfig

class MarketrecordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketrecord'

    def ready(self):
        print("Marketrecord app is ready!")
        import marketrecord.signals  # This will ensure the signal handlers are connected