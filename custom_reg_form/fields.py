import logging

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from student_account.fields import AccountSettingsExtensionField

from .models import InterSystemsUserProfile

logger = logging.getLogger(__name__)


class CMCUsernameExtensionField(AccountSettingsExtensionField):

    field_id = 'organization'
    js_model = 'js/student_account/models/user_account_model'
    js_field_view_class = 'FieldViews.StringFieldView'
    api_url = None
    title = 'Organisation'
    helpMessage = 'The organisation through which you provide care.'
    valueAttribute = 'organization'
    persistChanges = True 

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