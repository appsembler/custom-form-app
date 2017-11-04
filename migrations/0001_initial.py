# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InterSystemsUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.CharField(max_length=100, verbose_name=b'Organization', blank=True)),
                ('job_title', models.CharField(max_length=100, verbose_name=b'Job Title', blank=True)),
                ('user', models.ForeignKey(unique=True, related_name='InterSystemspreferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]