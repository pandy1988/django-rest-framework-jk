from uuid import UUID

from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from rest_framework_jk.settings import api_settings
from rest_framework_jk.compat import verify_auth_key, verify_access_key

# Create your authentications here.

class BaseJKAuthentication(BaseAuthentication):
    """
    Simple key based authentication.
    Clients should authenticate by passing the key in the "Authorization".
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            return None
        if not auth[0].lower() == self.keyword.lower().encode():
            return None
        # Confirm the number of fields in the authorization header.
        if len(auth) == 1:
            message = _('Invalid %s header. No credentials provided.' % self.keyword)
            raise AuthenticationFailed(message)
        if len(auth) > 2:
            message = _('Invalid %s header. Key string should not contain spaces.' % self.keyword)
            raise AuthenticationFailed(message)
        # Confirm the key is UUID.
        try:
            key = UUID(auth[1].decode()).hex
        except:
            message = _('Invalid %s header. Key string is not a valid UUID.' % self.keyword)
            raise AuthenticationFailed(message)
        return self.authenticate_credentials(key)

    def authenticate_credentials(self, key):
        if not key:
            message = _('Invalid key.')
            raise AuthenticationFailed(message)
        if not key.owner.is_active:
            message = _('This key is disabled.')
            raise AuthenticationFailed(message)
        return (key.owner, key)


class AuthKeyAuthentication(BaseJKAuthentication):
    """
    It authenticates using the authentication key.
    """
    keyword = api_settings.AUTH_HEADER_PREFIX

    def authenticate_credentials(self, key):
        auth_key = verify_auth_key(key)
        return super(AuthKeyAuthentication, self).authenticate_credentials(auth_key)


class AccessKeyAuthentication(BaseJKAuthentication):
    """
    It authenticates using the access key.
    """
    keyword = api_settings.ACCESS_HEADER_PREFIX

    def authenticate_credentials(self, key):
        access_key = verify_access_key(key)
        return super(AccessKeyAuthentication, self).authenticate_credentials(access_key)
