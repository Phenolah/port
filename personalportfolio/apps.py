from django.apps import AppConfig


class PersonalportfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personalportfolio'
    
        def ready(self):
        import signals

