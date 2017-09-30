from django.db import models
from django.utils.text import slugify
from accounts.models import  Team, UserProfile
from django.contrib.auth import get_user_model
from tags.models import Tags
User = get_user_model()

from django.conf import settings
# Create your models here.
class NewsPaper(models.Model):
    Paper_name=models.CharField(max_length=50)
    slug=models.SlugField(allow_unicode=True)
    paper_url=models.URLField(max_length=100)
    active=models.BooleanField()

    def __str__(self):
        return self.Paper_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Paper_name)
        super().save(*args, **kwargs)
# TO DO
    # def get_absolute_url(self):
    #     return reverse("news:", kwargs={"slug": self.slug})


class News(models.Model):
    title= models.CharField(max_length=50, unique=True)
    text= models.CharField(max_length=2000)
    news_url= models.URLField(max_length=250)
    image=models.ImageField(blank=True,null=True, default='E:\01_web_dev\simple_social_clone\simplesocial\static\images\img.jpg')
    image_url=models.URLField(default='https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Django_logo.svg/1200px-Django_logo.svg.png')
    source=models.ForeignKey(NewsPaper,related_name='newspapers')
    team=models.ManyToManyField(Team,through='NewsTeam')
    date_added=models.DateTimeField()
    date_crawled=models.DateTimeField(auto_now=True)
    users=models.ManyToManyField(UserProfile,through='UserViewedNews')
    news_tags=models.ManyToManyField(Tags,through='NewsTags')

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
