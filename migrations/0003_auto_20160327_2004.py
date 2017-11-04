# -*- coding: utf-8 -*-
import json

from django.db import migrations


def get_models(apps):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("student", "UserProfile")
    InterSystemsUserProfile = apps.get_model("iscedxreports", "InterSystemsUserProfile")
    return (User, UserProfile, InterSystemsUserProfile)

def create_intersystemsuserprofile_record(apps, schema_editor):
    """ create a new InterSystemsUserProfile record for each UserProfile,
        setting Organization if available.
    """
    (User, UserProfile, InterSystemsUserProfile) = get_models(apps)
    for up in UserProfile.objects.all():
        user = User.objects.get(id=up.user_id)
        
        # make sure we don't already have an InterSystemsUserProfile obj
        try:
            iup = InterSystemsUserProfile.objects.get(user=user) 
            iup  # pyflakes
        except InterSystemsUserProfile.DoesNotExist:
            try:
                newp = InterSystemsUserProfile(user=user, organization=up.organization)
            except AttributeError:
                newp = InterSystemsUserProfile(user=user, organization='')
            newp.save()


def move_job_title_meta(apps, schema_editor):
    """ migrate job_title field from UserProfile meta JSON to InterSystemsUserProfile
        object field.
    """
    (User, UserProfile, InterSystemsUserProfile) = get_models(apps)
    for up in UserProfile.objects.all():
        try:
            meta = json.loads(up.meta)
            job_title = meta['job-title']
            if job_title:
                user = User.objects.get(id=up.user_id)
                iup = InterSystemsUserProfile.objects.get(user=user)  # one should already exist
                iup.job_title = job_title
                iup.save()
        except (ValueError, KeyError):  # only CMC microsites gave job-title meta
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('iscedxreports', '0002_auto_20160325_1608'),
        ('student', '0002_auto_20151208_1034'),
    ]

    operations = [
        migrations.RunPython(create_intersystemsuserprofile_record),
        migrations.RunPython(move_job_title_meta),
    ]
