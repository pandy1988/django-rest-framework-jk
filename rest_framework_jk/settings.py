from datetime import timedelta

from django.conf import settings

from rest_framework.settings import APISettings

# Create your settings here.

USER_SETTINGS = getattr(settings, 'REST_FRAMEWORK_JK', None)

DEFAULTS = {
    'AUTH_EXPIRATION_DELTA': timedelta(days=1),
    'REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    'AUTH_HEADER_PREFIX': 'JK-Auth',
    'ACCESS_HEADER_PREFIX': 'JK-Access',
}

IMPORT_SETTINGS = ()

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_SETTINGS)
