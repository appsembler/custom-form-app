from django.conf import settings
from django.db import models

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class InterSystemsUserProfile(models.Model):
    """
    User profile fields specific to InterSystems
    """
    user = models.OneToOneField(USER_MODEL, related_name= "InterSystemspreferences", null=True, )
    organization = models.CharField(verbose_name='Organisation', blank=False, null=True, max_length=100)
    job_title = models.CharField(verbose_name='Job Title', blank=True, null=True, max_length=100)
    cmc_username = models.CharField(verbose_name='CMC Username', blank=True, null=True, max_length=100)
