from django.conf.urls import patterns, url

# added via APPSEMBLER FEATURE LMS_URLS_INCLUDE
# ^api/v1/cmcuserprofile/

USERNAME_PATTERN = r'(?P<username>[\w.+-]+)'


urlpatterns = patterns(
    'custom_reg_form.views',
    url(r'^/{}$'.format(USERNAME_PATTERN),
    	views.CMCUserProfile.as_view(), 
    	name='cmcuserprofile_api'
    ),
)
