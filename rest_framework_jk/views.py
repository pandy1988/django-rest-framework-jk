from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_jk import models, serializers

# Create your views here.


class AuthKeyViewSet(viewsets.GenericViewSet):
    """
    Viewset of authentication key.
    """
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ObtainAuthKeySerializer
        elif self.action == 'refresh':
            return serializers.RefreshAuthKeySerializer
        return serializers.AuthKeySerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        auth_key, void = models.AuthKey.objects.update_or_create(owner=user)
        refresh_key, void = models.RefreshKey.objects.update_or_create(owner=user)
        return Response({'auth_key': auth_key.key, 'refresh_key': refresh_key.key})

    @action(detail=False, methods=['put', 'patch'])
    def refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_key = serializer.validated_data.get('auth_key')
        refresh_key = serializer.validated_data.get('refresh_key')
        auth_key.key = auth_key.generate_key
        auth_key.save()
        refresh_key.key = refresh_key.generate_key
        refresh_key.save()
        return Response({'auth_key': auth_key.key, 'refresh_key': refresh_key.key})


class AccessKeyViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
    Viewset of access key.
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.AccessKey.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'refresh':
            return serializers.RefreshAccessKeySerializer
        return serializers.AccessKeySerializer

    @action(detail=True, methods=['put', 'patch'])
    def refresh(self, request, pk=None):
        access_key = self.get_object()
        access_key.key = access_key.generate_key
        access_key.save()
        return Response({'access_key': access_key.key})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
