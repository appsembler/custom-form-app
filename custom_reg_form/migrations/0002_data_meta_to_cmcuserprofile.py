# -*- coding: utf-8 -*-
from copy import deepcopy
import json
import logging

from django.db import migrations


logger = logging.getLogger(__name__)


def get_models(apps):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("student", "UserProfile")
    CMCUserProfile = apps.get_model("custom_reg_form", "CMCUserProfile")
    return (User, UserProfile, CMCUserProfile)


def move_job_title_and_organization_from_meta(apps, schema_editor):
    """ migrate cmc_userprofile, job_title and organization fields from 
        UserProfile meta field to CMCUserProfile.
    """

    (User, UserProfile, CMCUserProfile) = get_models(apps)
    for up in UserProfile.objects.all():
        try:
            meta = json.loads(up.meta)
        except ValueError:
            meta = {}
        try:
            org = meta.get('organization', None)
            job_title = meta.get('job-title', None)
            cmc_username = meta.get('cmc_username', None)            
            user = User.objects.get(id=up.user.id)

            (cup, created) = CMCUserProfile.objects.get_or_create(user=user)
            # don't overwrite existing value if exists
            cup.organization = org if not cup.organization else cup.organization
            cup.job_title = job_title if not cup.job_title else cup.job_title
            cup.cmc_username = cmc_username if not cup.cmc_username else cup.cmc_username
            cup.save()
            new_meta = deepcopy(meta)
            new_meta.pop('organization', None)
            new_meta.pop('job-title', None)
            new_meta.pop('cmc_username', None)
            up.meta = json.dumps(new_meta)
            up.save()
        except (ValueError, KeyError), e:
            logger.warn("Couldn't create a CMCUserProfile for user {}. Kept old values in UserProfile.meta. Error: {}".format(up.user.username, str(e)))
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('custom_reg_form', '0001_initial'),
        ('student', '0002_auto_20151208_1034'),
    ]

    operations = [
        migrations.RunPython(move_job_title_and_organization_from_meta),
    ]
