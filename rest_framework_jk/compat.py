from django.utils.timezone import now

from rest_framework_jk.settings import api_settings
from rest_framework_jk.models import AuthKey, RefreshKey, AccessKey

# Create your methods here.

def verify_auth_key(key, precise=True):
    """
    Confirm that the authentication key is valid.

    :param str key: Authentication key string.
    :param bool precise: Precise check mode.
    """
    expiration = now() - api_settings.AUTH_EXPIRATION_DELTA
    try:
        if precise:
            auth_key = AuthKey.objects.get(key=key, updated_at__gte=expiration)
        else:
            auth_key = AuthKey.objects.get(key=key)
    except:
        return None
    else:
        return auth_key


def verify_refresh_key(key):
    """
    Confirm that the refresh key is valid.

    :param str key: Refresh key string.
    """
    expiration = now() - api_settings.REFRESH_EXPIRATION_DELTA
    try:
        refresh_key = RefreshKey.objects.get(key=key, updated_at__gte=expiration)
    except:
        return None
    else:
        return refresh_key


def verify_access_key(key):
    """
    Confirm that the access key is valid.

    :param str key: Access key string.
    """
    try:
        access_key = AccessKey.objects.get(key=key)
    except:
        return None
    else:
        return access_key
