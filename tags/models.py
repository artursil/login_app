from django.db import models
from django.utils.text import slugify
# from news.models import NewsPaper
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

class League(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug=models.SlugField(allow_unicode=True,default="default")
    full_name = models.CharField(max_length=50, unique=True,blank=True,null=True)
    league = models.ForeignKey(League, related_name="leagues")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tags(models.Model):

    tag_name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(allow_unicode=True)
    main_tag=models.CharField(max_length=50,null=True, blank=True)
    team=models.ForeignKey(Team,blank=True,null=True)
    league=models.ForeignKey(League,blank=True,null=True )
    newspaper=models.ForeignKey(NewsPaper,blank=True,null=True)


    def __str__(self):
        return self.tag_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag_name)
        super().save(*args, **kwargs)
