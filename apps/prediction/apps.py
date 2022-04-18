from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class PredictionConfig(AppConfig):
    label = 'prediction'
    name = 'apps.prediction'
    verbose_name = _('Prediction')
