from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class AbstractKey(models.Model):
    """
    This is an abstract class that defines the basic items of the key model.
    """
    id = models.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    key = models.UUIDField(
        verbose_name=_('Key'),
        default=uuid4,
        unique=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.key

    @property
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
        'auth.User',
        verbose_name=_('Owner'),
        related_name=_('auth_key'),
        on_delete=models.CASCADE,
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
        'auth.User',
        verbose_name=_('Owner'),
        related_name=_('refresh_key'),
        on_delete=models.CASCADE,
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
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        blank=True,
    )
    owner = models.ForeignKey(
        'auth.User',
        verbose_name=_('Owner'),
        related_name=_('access_keys'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Access key')
        verbose_name_plural = _('Access keys')
        db_table = 'jk_access_keys'
