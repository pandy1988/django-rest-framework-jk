from django.utils.translation import ugettext as _

from rest_framework import serializers
from rest_framework.compat import authenticate
from rest_framework.exceptions import PermissionDenied

from rest_framework_jk import models, compat

# Create your serializers here.


class AuthKeySerializer(serializers.Serializer):
    """
    Serializer of authentication key.
    """
    pass


class ObtainAuthKeySerializer(serializers.Serializer):
    """
    Serializer of obtain authentication key.
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

        request = self.context.get('request')
        user = authenticate(request=request, username=username, password=password)

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

        attrs['user'] = user
        return attrs


class RefreshAuthKeySerializer(serializers.Serializer):
    """
    Serializer of refresh authentication key.
    """
    auth_key = serializers.UUIDField(
        label=_('Auth key'),
        write_only=True,
    )
    refresh_key = serializers.UUIDField(
        label=_('Refresh key'),
        write_only=True,
    )

    def validate(self, attrs):
        auth_key = attrs.get('auth_key')
        refresh_key = attrs.get('refresh_key')

        verified_auth_key = compat.verify_auth_key(auth_key.hex, precise=False)
        verified_refresh_key = compat.verify_refresh_key(refresh_key.hex)

        if not verified_auth_key or not verified_refresh_key:
            message = _('Invalid in with provided credentials.')
            raise PermissionDenied(message, code='verify_refresh_key')

        # Make sure the credentials are the same user.
        if not verified_auth_key.owner == verified_refresh_key.owner:
            message = _('The credentials were inconsistent.')
            raise PermissionDenied(message, code='verify_refresh_key')

        attrs['auth_key'] = verified_auth_key
        attrs['refresh_key'] = verified_refresh_key
        return attrs


class AccessKeySerializer(serializers.ModelSerializer):
    """
    Serializer of access key.
    """
    key = serializers.UUIDField(
        read_only=True,
    )

    class Meta:
        model = models.AccessKey
        fields = ('id', 'key', 'name')


class RefreshAccessKeySerializer(serializers.Serializer):
    """
    Serializer of refresh access key.
    """
    pass
