# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-08 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20170708_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='tweet_source',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='news',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
