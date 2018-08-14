# django-rest-framework-jk

This authentication scheme uses a simple `UUID-key-based` HTTP Authentication scheme.

Key authentication is appropriate for client-server setups, such as native desktop and mobile clients.

## Requirements

- Python 3.5+

- Django 2.0+

- Django REST Framework 3.0+

## Installation

Install using pip.

```
# pip install git+https://github.com/pandy1988/django-rest-framework-jk
```

## Usage

To use the authentication scheme you'll include `rest_framework_jk` in your `INSTALLED_APPS` setting.

Make sure to run `manage.py migrate` after changing your settings.

```python
INSTALLED_APPS = [
    # ....
    'rest_framework_jk',
]
```

Additionally `AuthKeyAuthentication` or `AccessKeyAuthentication` to Django REST framework's `DEFAULT_AUTHENTICATION_CLASSES`.

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # ....
        'rest_framework_jk.authentication.AuthKeyAuthentication',
        'rest_framework_jk.authentication.AccessKeyAuthentication',
    ),
}
```

Add the following URL route to `urls.py` and activate the key handling methods.

```python
urlpatterns = [
    # ....
    path('key/', include('rest_framework_jk.urls')),
]
```

## Authentication Key

The user can have only one authentication key.

**Obtain**

```
# curl -X POST -H 'Content-Type: application/json' -d '{
    "username": "....",
    "password": "...."
}' http://localhost/key/auth-obtain
```

```
# curl -X POST -H 'Authorization: JK-Auth ........' http://localhost/api/method
```

**Verify**

```
# curl -X POST -H 'Content-Type: application/json' -d '{
    "auth_key": "........"
}' http://localhost/key/auth-verify
```

**Refresh**

```
# curl -X POST -H 'Content-Type: application/json' -d '{
    "auth_key": "........",
    "refresh_key": "........"
}' http://localhost/key/auth-refresh
```

## Access Key

A user can have multiple access keys.

**Obtain**

```
# curl -X POST -H 'Content-Type: application/json' -d '{
    "username": "....",
    "password": "...."
}' http://localhost/key/access-obtain
```

```
# curl -X POST -H 'Authorization: JK-Access ........' http://localhost/api/method
```

**Refresh**

```
# curl -X POST -H 'Content-Type: application/json' -d '{
    "username": "....",
    "password": "....",
    "access_key": "........"
}' http://localhost/key/access-refresh
```

**Destory**

```
# curl -X POST -H 'Content-Type: application/json' -d '{
    "username": "....",
    "password": "....",
    "access_key": "........"
}' http://localhost/key/access-destroy
```

## Settings

```python
REST_FRAMEWORK_JK = {
    # This is the expiration date of the keys.
    'AUTH_EXPIRATION_DELTA': timedelta(days=1),
    'REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    # Another value used for the authorization header to distinguish keys.
    'AUTH_HEADER_PREFIX': 'JK-Auth',
    'ACCESS_HEADER_PREFIX': 'JK-Access',
}
```

## Author

[@pandy1988](https://github.com/pandy1988)
