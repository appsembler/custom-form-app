from rest_framework import serializers
from openedx.core.djangoapps.user_api.serializers import ReadOnlyFieldsSerializerMixin

from .models import InterSystemsUserProfile


class CMCUserProfileSerializer(serializers.HyperlinkedModelSerializer, ReadOnlyFieldsSerializerMixin):
    """
    Class that serializes the portion of User model needed for account information.
    """
    class Meta:
        model = CMCUserProfile
        fields = ("organization", "job_title", "cmc_username")
        # read_only_fields = ()
        # explicit_read_only_fields = ()
