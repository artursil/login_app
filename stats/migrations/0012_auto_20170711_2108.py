# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_gameevents_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameevents',
            name='home',
            field=models.BooleanField(),
        ),
    ]
