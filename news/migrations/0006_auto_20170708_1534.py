# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-08 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20170708_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='fb_post',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='news',
            name='meme',
            field=models.BooleanField(default=False),
        ),
    ]
