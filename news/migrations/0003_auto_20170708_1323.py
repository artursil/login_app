# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-08 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20170704_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='tweet',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='news',
            name='image_url',
            field=models.URLField(),
        ),
    ]
