from .models import ExtraInfo
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.forms.fields import CharField

class ExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model in models.py.
    """
    guid = CharField(widget=HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        super(ExtraInfoForm, self).__init__(*args, **kwargs)

    class Meta(object):
        model = ExtraInfo
        fields = ('phone', 'guid')
