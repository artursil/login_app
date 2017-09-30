from django.db import models
from django.utils.text import slugify
from accounts.models import UserProfile
from django.contrib.auth import get_user_model
from tags.models import Tags, Team, NewsPaper
User = get_user_model()

from django.conf import settings
# Create your models here.



class News(models.Model):
    title= models.CharField(max_length=50, unique=True)
    text= models.CharField(max_length=2000)
    news_url= models.URLField(max_length=250)
    image=models.ImageField(blank=True,null=True)
    image_url=models.URLField(blank=True,null=True)
    tweet=models.BooleanField(default=False)
    social_source=models.CharField(max_length=100,blank=True)
    fb_post=models.BooleanField(default=False)
    meme=models.BooleanField(default=False)
    source=models.ForeignKey(NewsPaper,related_name='newspapers',null=True,blank=True)
    team=models.ManyToManyField(Team,through='NewsTeam')
    date_added=models.DateTimeField()
    date_crawled=models.DateTimeField(auto_now=True)
    users=models.ManyToManyField(UserProfile,through='UserViewedNews')
    news_tags=models.ManyToManyField(Tags,through='NewsTags')
    favs=models.IntegerField(blank=True,null=True)
    retweets=models.IntegerField(blank=True,null=True)
    replies=models.IntegerField(blank=True,null=True)
    fb_rating = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.title


    class Meta:
        ordering = ["-date_added"]

class NewsTeam(models.Model):
    news=models.ForeignKey(News,related_name="newsteams")
    team=models.ForeignKey(Team,related_name='teamnews')

    def __str__(self):
        return "{}_{}".format(self.news.pk,self.team.name)

    class Meta:
        unique_together = ("news", "team")

class UserViewedNews(models.Model):
    user=models.ForeignKey(UserProfile,related_name="usernews")
    news=models.ForeignKey(News,related_name="newsuser")
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}_{}".format(self.user,self.news.title[:10])

    class Meta:
        unique_together = ("news", "user")


class NewsTags(models.Model):
    news=models.ForeignKey(News,related_name="newstags")
    tag=models.ForeignKey(Tags)

    def __str__(self):
        return "{}_{}".format(self.news.pk,self.tag.tag_name)
    class Meta:
        unique_together = ("tag", "news")
