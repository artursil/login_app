# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-04 18:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('text', models.CharField(max_length=2000)),
                ('news_url', models.URLField(max_length=250)),
                ('image', models.ImageField(blank=True, default='E:\x01_web_dev\\simple_social_clone\\simplesocial\\static\\images\\img.jpg', null=True, upload_to='')),
                ('image_url', models.URLField(default='https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Django_logo.svg/1200px-Django_logo.svg.png')),
                ('date_added', models.DateTimeField()),
                ('date_crawled', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='NewsTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newstags', to='news.News')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.Tags')),
            ],
        ),
        migrations.CreateModel(
            name='NewsTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newsteams', to='news.News')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamnews', to='tags.Team')),
            ],
        ),
        migrations.CreateModel(
            name='UserViewedNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newsuser', to='news.News')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usernews', to='accounts.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='news_tags',
            field=models.ManyToManyField(through='news.NewsTags', to='tags.Tags'),
        ),
        migrations.AddField(
            model_name='news',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newspapers', to='tags.NewsPaper'),
        ),
        migrations.AddField(
            model_name='news',
            name='tmp',
            field=models.ManyToManyField(through='news.NewsTeam', to='tags.Team'),
        ),
        migrations.AddField(
            model_name='news',
            name='users',
            field=models.ManyToManyField(through='news.UserViewedNews', to='accounts.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='userviewednews',
            unique_together=set([('news', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='newsteam',
            unique_together=set([('news', 'team')]),
        ),
        migrations.AlterUniqueTogether(
            name='newstags',
            unique_together=set([('tag', 'news')]),
        ),
    ]
