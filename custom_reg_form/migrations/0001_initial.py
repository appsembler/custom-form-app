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
            name='CMCUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.CharField(max_length=100, null=True, verbose_name=b'Organisation')),
                ('job_title', models.CharField(max_length=100, null=True, verbose_name=b'Job Title', blank=True)),
                ('cmc_username', models.CharField(max_length=100, null=True, verbose_name=b'CMC Username', blank=True)),
                ('user', models.OneToOneField(related_name='InterSystemspreferences', null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
