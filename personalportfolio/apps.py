from django.apps import AppConfig


class PersonalportfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personalportfolio'
    
class MeasurementConfig(AppConfig):
    name = 'measurements'
    verbose_name = 'Measurement between 2 locations'


