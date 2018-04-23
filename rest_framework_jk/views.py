from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_jk.models import AuthKey, RefreshKey, AccessKey
from rest_framework_jk.serializers import (
    AuthSerializer,
    VerifyAuthKeySerializer, RefreshAuthKeySerializer,
    AccessKeySerializer,
)

# Create your views here.

class ObtainAuthKey(APIView):
    """
    Issue the authentication key and refresh key.
    """
    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={ 'request': request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        auth_key, void = AuthKey.objects.update_or_create(owner=user)
        refresh_key, void = RefreshKey.objects.update_or_create(owner=user)
        return Response({ 'auth_key': auth_key.key, 'refresh_key': refresh_key.key })


class VerifyAuthKey(APIView):
    """
    Confirm that the authentication key is valid.
    """
    serializer_class = VerifyAuthKeySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({ 'success': 'auth_key' in serializer.validated_data })


class RefreshAuthKey(APIView):
    """
    Refresh the authentication key.
    """
    serializer_class = RefreshAuthKeySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_key = serializer.validated_data['auth_key']
        refresh_key = serializer.validated_data['refresh_key']
        auth_key.save()
        refresh_key.save()
        return Response({ 'auth_key': auth_key.key, 'refresh_key': refresh_key.key })


class ObtainAccessKey(APIView):
    """
    Issue the access key.
    """
    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        access_key = AccessKey.objects.create(owner=user)
        return Response({ 'access_key': access_key.key })


class RefreshAccessKey(APIView):
    """
    Refresh the access key.
    """
    serializer_class = AccessKeySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_key = serializer.validated_data['access_key']
        access_key.save()
        return Response({ 'access_key': access_key.key })


class DestroyAccessKey(APIView):
    """
    Destroy the access key.
    """
    serializer_class = AccessKeySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_key = serializer.validated_data['access_key']
        count, void = access_key.delete()
        return Response({ 'success': count == 1 })
