# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-09 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0005_remove_tags_negative'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='other_tags',
        ),
        migrations.AddField(
            model_name='tags',
            name='main_tag',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]