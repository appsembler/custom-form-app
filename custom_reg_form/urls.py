from django.conf.urls import patterns, url

from custom_reg_form.views import CMCUserProfileView

# added via APPSEMBLER FEATURE LMS_URLS_INCLUDE
# ^api/v1/cmcuserprofile/

USERNAME_PATTERN = r'(?P<username>[\w.+-]+)'


urlpatterns = patterns(
    'custom_reg_form.views',
    url(r'^/{}$'.format(USERNAME_PATTERN),
    	CMCUserProfileView.as_view(), 
    	name='cmcuserprofile_api'
    ),
)
