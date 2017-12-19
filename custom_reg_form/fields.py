import logging

from django.core.urlresolvers import reverse

from student_account.fields import AccountSettingsExtensionField


logger = logging.getLogger(__name__)


# overrideable properties are 
# ['label', 'type', 'defaultValue', 'placeholder', 'instructions', 'required', 'restrictions', 'options', 'supplementalLink', 'supplementalText']
REG_FORM_FIELD_OVERRIDES = {
    'name': {
        'label': "Full Name",
        'placeholder': "",
        'instructions': ""
    },
    'terms_of_service': {
        'label': "I have read and agree to the <a target='register_extra' href='/tos'>Terms and Conditions</a> and <a target='register_extra' class='new-vp' href='/privacy'>Privacy Policy</a>",
        'instructions': '',
        'supplementalLink': '',
        'supplementalText': ''
    },
    'username': {
        'required': False,
        'type': 'hidden',
        'label': '',
        'instructions': '',
    }
}


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
            'options': getattr(self, 'options', None),
            'persistChanges': self.persistChanges
        }


class CMCOrganizationExtensionField(CMCBaseExtensionField):

    field_id = 'organization'
    js_model = 'js/student_account/models/user_account_model'
    js_field_view_class = 'AccountSettingsFieldViews.TextFieldView'
    api_url = None
    title = 'Organisation'
    helpMessage = 'The name of your organisation'
    valueAttribute = 'organization'
    persistChanges = True


class CMCUsernameExtensionField(CMCBaseExtensionField):

    field_id = 'cmc_username'
    js_model = 'js/student_account/models/user_account_model'
    js_field_view_class = 'AccountSettingsFieldViews.TextFieldView'
    api_url = None
    title = 'CMC Username'
    helpMessage = 'Your CMC username (if available)'
    valueAttribute = 'cmc_username'
    persistChanges = True


class CMCJobTitleExtensionField(CMCBaseExtensionField):

    field_id = 'job_title'
    js_model = 'js/student_account/models/user_account_model'
    js_field_view_class = 'AccountSettingsFieldViews.TextFieldView'
    api_url = None
    title = 'Job Title'
    helpMessage = 'Your job title'
    valueAttribute = 'job_title'
    persistChanges = True
