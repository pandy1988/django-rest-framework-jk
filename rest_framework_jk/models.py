from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

# Create your models here.

UserModel = get_user_model()


class AbstractKey(models.Model):
    """
    This is an abstract class that defines the basic items of the key model.
    """
    id = models.AutoField(
        verbose_name = _('ID'),
        primary_key = True,
    )
    key = models.CharField(
        verbose_name = _('Key'),
        max_length = 32,
        unique = True,
    )
    updated_at = models.DateTimeField(
        verbose_name = _('Updated at'),
        auto_now = True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.key

    def save(self, *args, **kwargs):
        self.key = self.generate_key()
        return super(AbstractKey, self).save(*args, **kwargs)

    def generate_key(self):
        """
        To generate a unique key, use uuid4.
        """
        return uuid4().hex


class AuthKey(AbstractKey):
    """
    This is the model that defines the authentication key.
    Authentication key shall be used from the front end.
    The user can have only one authentication key.
    """
    owner = models.OneToOneField(
        UserModel,
        verbose_name = _('Owner'),
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name = _('Auth key')
        verbose_name_plural = _('Auth keys')
        db_table = 'jk_auth_keys'


class RefreshKey(AbstractKey):
    """
    This is the model that defines the refresh key.
    Refresh keys are used to update the same user's authentication key.
    The user can have only one refresh key.
    """
    owner = models.OneToOneField(
        UserModel,
        verbose_name = _('Owner'),
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name = _('Refresh key')
        verbose_name_plural = _('Refresh keys')
        db_table = 'jk_refresh_keys'


class AccessKey(AbstractKey):
    """
    This is the model that defines the access key.
    Access key shall be used from the other systems.
    A user can have multiple access keys.
    """
    owner = models.ForeignKey(
        UserModel,
        verbose_name = _('Owner'),
        related_name = _('access_key_owner_belongs_to_user'),
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name = _('Access key')
        verbose_name_plural = _('Access keys')
        db_table = 'jk_access_keys'
