# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-08 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_team_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='negative',
            field=models.BooleanField(default=False),
        ),
    ]