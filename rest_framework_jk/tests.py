from uuid import uuid4
from time import sleep
from datetime import timedelta
from functools import reduce

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_jk import views
from rest_framework_jk.settings import api_settings
from rest_framework_jk.authentication import AuthKeyAuthentication, AccessKeyAuthentication

# Create your tests here.

UserModel = get_user_model()
factory = APIRequestFactory()


class Dict(dict):
    """
    Expand dictionary instances.
    """

    def merge(self, *args):
        """
        Merge the dictionary instances into one.
        """
        return reduce(lambda a, b: Dict(a, **b), args, self)

    def fkeys(self, keys):
        """
        Filter the dictionary instance with the specified keys.

        :param set keys: Filter condition for keys.
        """
        return Dict({key: value for key, value in self.items() if key in keys})


class BaseTestCase(APITestCase):
    """
    Base test case.
    """

    def setUp(self):
        # Valid case
        self.valid_credentials = Dict({
            'username': 'valid-username',
            'password': 'valid-password',
            'email': 'valid-email@example.com',
        })
        self.valid_user = UserModel.objects.create_user(**self.valid_credentials)

        # Invalid case
        self.invalid_credentials = Dict({
            'username': 'invalid-username',
            'password': 'invalid-password',
            'email': 'invalid-email@example.com',
        })
        self.invalid_user = UserModel(**self.invalid_credentials)

    def get_valid_user_pass(self):
        return self.valid_credentials.fkeys({'username', 'password'})

    def get_invalid_user_pass(self):
        return self.invalid_credentials.fkeys({'username', 'password'})


class AuthKeyTestCase(BaseTestCase):
    """
    Test authentication key case.
    """

    def authenticate(self, key):
        authentication = AuthKeyAuthentication()

        try:
            authentication.authenticate_credentials(key)
        except AuthenticationFailed:
            return False

        return True

    def test_auth_obtain(self):
        url = reverse('auth-list')
        view = views.AuthKeyViewSet.as_view({'post': 'create'})

        # Valid case
        valid_request = factory.post(url, self.get_valid_user_pass())
        valid_response = view(valid_request)
        self.assertEqual(valid_response.status_code, HTTP_200_OK)
        self.assertEqual(valid_response.data.keys(), {'auth_key', 'refresh_key'})
        self.assertTrue(self.authenticate(valid_response.data['auth_key']))

        # Invalid case
        invalid_request = factory.post(url, self.get_invalid_user_pass())
        invalid_response = view(invalid_request)
        self.assertEqual(invalid_response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(invalid_response.data.keys(), {'detail'})

        return (Dict(**valid_response.data), Dict(**invalid_response.data))

    def test_auth_refresh(self):
        url = reverse('auth-refresh')
        view = views.AuthKeyViewSet.as_view({'put': 'refresh', 'patch': 'refresh'})
        valid_data, invalid_data = self.test_auth_obtain()

        # Valid case
        valid_request = factory.patch(url, valid_data.fkeys({'auth_key', 'refresh_key'}))
        valid_response = view(valid_request)
        self.assertEqual(valid_response.status_code, HTTP_200_OK)
        self.assertEqual(valid_response.data.keys(), {'auth_key', 'refresh_key'})
        self.assertNotEqual(valid_response.data.get('auth_key'), valid_data.get('auth_key'))
        self.assertNotEqual(valid_response.data.get('refresh_key'), valid_data.get('refresh_key'))
        self.assertFalse(self.authenticate(valid_data.get('auth_key')))

        # Invalid case
        invalid_request = factory.patch(url, Dict({'auth_key': uuid4().hex, 'refresh_key': uuid4().hex}))
        invalid_response = view(invalid_request)
        self.assertEqual(invalid_response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(invalid_response.data.keys(), {'detail'})

    def test_auth_refresh_with_lapsed_auth_key(self):
        url = reverse('auth-refresh')
        view = views.AuthKeyViewSet.as_view({'put': 'refresh', 'patch': 'refresh'})
        valid_data, invalid_data = self.test_auth_obtain()

        # Shorten expiration date
        api_settings.AUTH_EXPIRATION_DELTA = timedelta(seconds=1)
        sleep(1)

        # Valid case
        valid_request = factory.patch(url, valid_data.fkeys({'auth_key', 'refresh_key'}))
        valid_response = view(valid_request)
        self.assertEqual(valid_response.status_code, HTTP_200_OK)
        self.assertEqual(valid_response.data.keys(), {'auth_key', 'refresh_key'})
        self.assertNotEqual(valid_response.data.get('auth_key'), valid_data.get('auth_key'))
        self.assertNotEqual(valid_response.data.get('refresh_key'), valid_data.get('refresh_key'))
        self.assertFalse(self.authenticate(valid_data.get('auth_key')))

        # Restore expiration date to default
        api_settings.AUTH_EXPIRATION_DELTA = api_settings.defaults['AUTH_EXPIRATION_DELTA']

    def test_auth_refresh_with_lapsed_refresh_key(self):
        url = reverse('auth-refresh')
        view = views.AuthKeyViewSet.as_view({'put': 'refresh', 'patch': 'refresh'})
        valid_data, invalid_data = self.test_auth_obtain()

        # Shorten expiration date
        api_settings.REFRESH_EXPIRATION_DELTA = timedelta(seconds=1)
        sleep(1)

        # Invalid case
        invalid_request = factory.patch(url, valid_data.fkeys({'auth_key', 'refresh_key'}))
        invalid_response = view(invalid_request)
        self.assertEqual(invalid_response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(invalid_response.data.keys(), {'detail'})

        # Restore expiration date to default
        api_settings.REFRESH_EXPIRATION_DELTA = api_settings.defaults['REFRESH_EXPIRATION_DELTA']


class AccessKeyTestCase(BaseTestCase):
    """
    Test access key case.
    """

    def authenticate(self, key):
        authentication = AccessKeyAuthentication()

        try:
            authentication.authenticate_credentials(key)
        except AuthenticationFailed:
            return False

        return True

    def test_access_obtain(self):
        url = reverse('access-list')
        view = views.AccessKeyViewSet.as_view({'post': 'create'})

        # Valid case
        valid_request = factory.post(url)
        valid_request.user = self.valid_user
        valid_response = view(valid_request)
        self.assertEqual(valid_response.status_code, HTTP_201_CREATED)
        self.assertEqual(valid_response.data.keys(), {'id', 'key', 'name'})
        self.assertTrue(self.authenticate(valid_response.data.get('key')))

        # Invalid case
        invalid_request = factory.post(url)
        invalid_response = view(invalid_request)
        self.assertEqual(invalid_response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(invalid_response.data.keys(), {'detail'})

        return (Dict(**valid_response.data), Dict(**invalid_response.data))

    def test_access_refresh(self):
        valid_data, invalid_data = self.test_access_obtain()

        url = reverse('access-refresh', kwargs={'pk': valid_data.get('id')})
        view = views.AccessKeyViewSet.as_view({'put': 'refresh', 'patch': 'refresh'})

        # Valid case
        valid_request = factory.patch(url)
        valid_request.user = self.valid_user
        valid_response = view(valid_request, pk=valid_data.get('id'))
        self.assertEqual(valid_response.status_code, HTTP_200_OK)
        self.assertEqual(valid_response.data.keys(), {'access_key'})
        self.assertNotEqual(valid_response.data.get('access_key'), valid_data.get('key'))
        self.assertFalse(self.authenticate(valid_data.get('key')))

        # Invalid case
        invalid_request = factory.patch(url)
        invalid_response = view(invalid_request, pk=valid_data.get('id'))
        self.assertEqual(invalid_response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(invalid_response.data.keys(), {'detail'})

    def test_access_destroy(self):
        valid_data, invalid_data = self.test_access_obtain()

        url = reverse('access-detail', kwargs={'pk': valid_data.get('id')})
        view = views.AccessKeyViewSet.as_view({'delete': 'destroy'})

        # Valid case
        valid_request = factory.delete(url)
        valid_request.user = self.valid_user
        valid_response = view(valid_request, pk=valid_data.get('id'))
        self.assertEqual(valid_response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(self.authenticate(valid_data.get('access_key')))

        # Invalid case
        invalid_request = factory.delete(url)
        invalid_response = view(invalid_request, pk=valid_data.get('id'))
        self.assertEqual(invalid_response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(invalid_response.data.keys(), {'detail'})
