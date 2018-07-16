# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_reg_form', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrainfo',
            name='favorite_editor',
        ),
        migrations.RemoveField(
            model_name='extrainfo',
            name='favorite_movie',
        ),
        migrations.AddField(
            model_name='extrainfo',
            name='guid',
            field=models.CharField(max_length=100, verbose_name=b'GUID', blank=True),
        ),
        migrations.AddField(
            model_name='extrainfo',
            name='phone',
            field=models.CharField(max_length=100, verbose_name=b'Phone', blank=True),
        ),
    ]
