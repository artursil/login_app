# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-10 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_auto_20170710_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='league_flg',
            field=models.BooleanField(default=False),
        ),
    ]