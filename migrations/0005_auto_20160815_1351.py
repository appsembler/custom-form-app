# -*- coding: utf-8 -*-
import json

from django.db import migrations


def get_models(apps):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("student", "UserProfile")
    InterSystemsUserProfile = apps.get_model("iscedxreports", "InterSystemsUserProfile")
    return (User, UserProfile, InterSystemsUserProfile)


def move_job_title_and_organization_to_meta(apps, schema_editor):
    """ migrate job_title and organization fields from InterSystemsUserProfile 
        back to UserProfile meta field. (can't use ISUProfile b/c of SSO
    """
    (User, UserProfile, InterSystemsUserProfile) = get_models(apps)
    for iup in InterSystemsUserProfile.objects.all():
        try:
            org = iup.organization
            job_title = iup.job_title
            if job_title or org:
                user = User.objects.get(id=iup.user.id)
                up = UserProfile.objects.get(user=user)  # one should already exist
                meta = json.loads(up.meta)
                meta['organization'] = org
                meta['job-title'] = job_title
                up.meta = json.dumps(meta)
                up.save()
                iup.organization = None
                iup.job_title = None
                iup.save()
        except (ValueError, KeyError):  # only CMC microsites gave job-title meta
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('iscedxreports', '0004_auto_20160412_2240'),
        ('student', '0002_auto_20151208_1034'),
    ]

    operations = [
        migrations.RunPython(move_job_title_and_organization_to_meta),
    ]
