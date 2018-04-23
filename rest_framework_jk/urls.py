from django.urls import path

from rest_framework_jk.views import (
    ObtainAuthKey, VerifyAuthKey, RefreshAuthKey,
    ObtainAccessKey, RefreshAccessKey, DestroyAccessKey,
)

# Create your urls here.

urlpatterns = [
    path('auth-obtain', ObtainAuthKey.as_view(), name='jk-auth-obtain'),
    path('auth-verify', VerifyAuthKey.as_view(), name='jk-auth-verify'),
    path('auth-refresh', RefreshAuthKey.as_view(), name='jk-auth-refresh'),
    path('access-obtain', ObtainAccessKey.as_view(), name='jk-access-obtain'),
    path('access-refresh', RefreshAccessKey.as_view(), name='jk-access-refresh'),
    path('access-destroy', DestroyAccessKey.as_view(), name='jk-access-destroy'),
]
