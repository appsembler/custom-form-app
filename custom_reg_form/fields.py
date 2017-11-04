import logging

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from student_account.fields import AccountSettingsExtensionField

from .models import CMCUserProfile

logger = logging.getLogger(__name__)



class CMCBaseExtensionField(AccountSettingsExtensionField):

    def __init__(self, request):
        self.api_url = reverse("cmcuserprofile_api", kwargs={'username': request.user.username})

    def __call__(self):
        return {
            'id': self.field_id,
            'js_model': self.js_model,
            'js_field_view_class': self.js_field_view_class,
            'api_url': self.api_url,
            'title': self.title,
            'helpMessage': self.helpMessage,
            'valueAttribute': self.valueAttribute,
            'options': self.options,
            'persistChanges': self.persistChanges
        }


class CMCOrganizationExtensionField(CMCBaseExtensionField):

    field_id = 'organization'
    js_model = 'js/student_account/models/user_account_model'
    js_field_view_class = 'FieldViews.TextFieldView'
    api_url = None
    title = 'Organisation'
    helpMessage = 'The organisation through which you provide care.'
    valueAttribute = 'organization'
    persistChanges = True


class CMCUsernameExtensionField(CMCBaseExtensionField):

    field_id = 'cmc_username'
    js_model = 'js/student_account/models/user_account_model'
    js_field_view_class = 'FieldViews.TextFieldView'
    api_url = None
    title = 'CMC Username'
    helpMessage = 'Your Coordinate My Care username (if known)'
    valueAttribute = 'cmc_username'
    persistChanges = True


class CMCJobTitleExtensionField(CMCBaseExtensionField):

    field_id = 'job_title'
    js_model = 'js/student_account/models/user_account_model'
    js_field_view_class = 'FieldViews.TextFieldView'
    api_url = None
    title = 'Job Title'
    helpMessage = 'Your Job Title at your CMC Organisation'
    valueAttribute = 'job_title'
    persistChanges = True
