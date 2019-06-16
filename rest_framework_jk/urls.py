from rest_framework import routers

from rest_framework_jk import views

# Create your urls here.

router = routers.DefaultRouter(trailing_slash=False)
router.register('auth', views.AuthKeyViewSet, base_name='auth')
router.register('access', views.AccessKeyViewSet, base_name='access')
urlpatterns = router.urls
