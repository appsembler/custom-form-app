from django.forms import ModelForm, CharField

from .models import CMCUserProfile


class CMCUserProfileExtensionForm(ModelForm):


    class Meta(object):
        model = CMCUserProfile
        fields = ('cmc_username', 'job_title', 'organization')

    cmc_username = CharField(
        label='CMC Username', 
        initial='Your CMC username, if available',
        required=False
    )
    job_title = CharField(
        label='Job Title', 
        initial='Your job title',
        required=False
    )
    organization = CharField(
        label='Organisation',  # UK spelling
        initial='Your organisation'
    )

    def __init__(self, *args, **kwargs):
        super(CMCUserProfileExtensionForm, self).__init__(*args, **kwargs)
        self.fields['organization'].error_messages = {
            "required": u"Please indicate your organisation.",
        }
