from django.urls import path

from rest_framework_jk import views

# Create your urls here.

urlpatterns = [
    path('auth-obtain', views.ObtainAuthKey.as_view(), name='jk-auth-obtain'),
    path('auth-verify', views.VerifyAuthKey.as_view(), name='jk-auth-verify'),
    path('auth-refresh', views.RefreshAuthKey.as_view(), name='jk-auth-refresh'),
    path('access-obtain', views.ObtainAccessKey.as_view(), name='jk-access-obtain'),
    path('access-refresh', views.RefreshAccessKey.as_view(), name='jk-access-refresh'),
    path('access-destroy', views.DestroyAccessKey.as_view(), name='jk-access-destroy'),
]
