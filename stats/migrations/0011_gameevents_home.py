# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_remove_game_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameevents',
            name='home',
            field=models.BooleanField(default=True),
        ),
    ]
