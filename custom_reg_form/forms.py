from django.forms import ModelForm, CharField

from .models import CMCUserProfile


class CMCUserProfileExtensionForm(ModelForm):


    class Meta(object):
        model = CMCUserProfile
        fields = ('cmc_username', 'job_title', 'organization')

    cmc_username = CharField(label='CMC Username')
    job_title = CharField(label='Job Title')
    organization = CharField(label='Organisation')  # UK spelling

    def __init__(self, *args, **kwargs):
        super(CMCUserProfileExtensionForm, self).__init__(*args, **kwargs)
        self.fields['organization'].error_messages = {
            "required": u"Please indicate your organisation.",
        }

