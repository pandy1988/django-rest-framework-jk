from django.utils.translation import ugettext as _

from rest_framework import serializers
from rest_framework.compat import authenticate
from rest_framework.exceptions import PermissionDenied, ValidationError

from rest_framework_jk.compat import verify_auth_key, verify_refresh_key, verify_access_key

# Create your serializers here.


class AuthSerializer(serializers.Serializer):
    """
    Serializer for user credentials.
    """
    username = serializers.CharField(
        label=_('Username'),
    )
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if user:
                # From Django onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    message = _('User account is disabled.')
                    raise PermissionDenied(message, code='authenticate')
            else:
                message = _('Unable to log in with provided credentials.')
                raise PermissionDenied(message, code='authenticate')
        else:
            message = _('Must include "username" and "password".')
            raise ValidationError(message, code='authenticate')

        attrs['user'] = user
        return attrs


class VerifyAuthKeySerializer(serializers.Serializer):
    """
    Serializer of authentication key.
    """
    auth_key = serializers.UUIDField(
        label=_('Auth key'),
        format='hex',
    )

    def validate(self, attrs):
        auth_key = attrs.get('auth_key')

        if auth_key:
            verified_auth_key = verify_auth_key(auth_key.hex)
            if not verified_auth_key:
                message = _('Invalid in with provided credentials.')
                raise PermissionDenied(message, code='verify_auth_key')
        else:
            message = _('Must include "auth_key".')
            raise ValidationError(message, code='verify_auth_key')

        attrs['auth_key'] = verified_auth_key
        return attrs


class RefreshAuthKeySerializer(VerifyAuthKeySerializer):
    """
    Serializer of refresh key.
    """
    refresh_key = serializers.UUIDField(
        label=_('Refresh key'),
        format='hex',
    )

    def validate(self, attrs):
        auth_key = attrs.get('auth_key')
        refresh_key = attrs.get('refresh_key')

        if auth_key and refresh_key:
            verified_auth_key = verify_auth_key(auth_key.hex, precise=False)
            verified_refresh_key = verify_refresh_key(refresh_key.hex)
            if not verified_auth_key or not verified_refresh_key:
                message = _('Invalid in with provided credentials.')
                raise PermissionDenied(message, code='verify_refresh_key')
            # Make sure the credentials are the same user.
            if not verified_auth_key.owner == verified_refresh_key.owner:
                message = _('The credentials were inconsistent.')
                raise PermissionDenied(message, code='verify_refresh_key')
        else:
            message = _('Must include "auth_key" and "refresh_key".')
            raise ValidationError(message, code='verify_refresh_key')

        attrs['auth_key'] = verified_auth_key
        attrs['refresh_key'] = verified_refresh_key
        return attrs


class AccessKeySerializer(AuthSerializer):
    """
    Serializer of access key.
    """
    access_key = serializers.UUIDField(
        label=_('Access key'),
        format='hex',
    )

    def validate(self, attrs):
        super(AccessKeySerializer, self).validate(attrs)
        user = attrs.get('user')
        access_key = attrs.get('access_key')

        if access_key:
            verified_access_key = verify_access_key(access_key.hex)
            if not verified_access_key:
                message = _('Invalid in with provided credentials.')
                raise PermissionDenied(message, code='verify_access_key')
            # Make sure the credentials are the same user.
            if not verified_access_key.owner == user:
                message = _('The credentials were inconsistent.')
                raise PermissionDenied(message, code='verify_access_key')
        else:
            message = _('Must include "access_key".')
            raise ValidationError(message, code='verify_access_key')

        attrs['access_key'] = verified_access_key
        return attrs
