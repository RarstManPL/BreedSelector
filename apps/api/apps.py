from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class ApiConfig(AppConfig):
    label = 'api'
    name = 'apps.api'
    verbose_name = _('API')
