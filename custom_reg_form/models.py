from django.conf import settings
from django.db import models

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ExtraInfo(models.Model):
    """
    This model contains two extra fields that will be saved when a user registers.
    The form that wraps this model is in the forms.py file.
    """
    user = models.OneToOneField(USER_MODEL, null=True)

    phone = models.CharField(
        verbose_name="Phone",
        max_length=100
    )

    guid = models.CharField(
        verbose_name="GUID",
        blank=True,
        max_length=100
    )
