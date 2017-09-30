from django.db import models
from tags.models import Team, League
from django.utils.text import slugify
# Create your models here.

class Season(models.Model):
    name=models.CharField(max_length=10)
    slug=models.SlugField(allow_unicode=True)
    date_start=models.DateField()
    date_end=models.DateField()

    def __str__(self):
        return self.name


class Stadium(models.Model):
    name=models.CharField(max_length=100, unique=True)
    capacity=models.IntegerField()
    city= models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Player(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    slug=models.SlugField(allow_unicode=True)
    dob=models.DateField()
    postition=models.CharField(max_length=3)
    team= models.ForeignKey(Team,related_name="player_team")
    active=models.BooleanField()

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

    def save(self, *args, **kwargs):
        tag = "{} {}".format(self.firstname, self.lastname)
        self.slug = slugify(tag)
        super().save(*args, **kwargs)

class Competition(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(allow_unicode=True)
    league=models.ForeignKey(League, blank=True, null=True)
    european=models.BooleanField()
    league_flg=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TeamStats(models.Model):
    team=models.ForeignKey(Team,related_name="stats_team")
    matches = models.IntegerField(default=0)
    wins=models.IntegerField()
    loses = models.IntegerField()
    draws= models.IntegerField()
    gf=models.IntegerField()
    ga=models.IntegerField()
    gd=models.IntegerField()
    points=models.IntegerField()
    season=models.ForeignKey(Season, null=True)
    competition =models.ForeignKey(Competition, related_name="competition_stats",null=True)

    def __str__(self):
        return "{}_stats".format(self.team)

    def save(self, *args, **kwargs):
        self.points = 3*self.wins + 1*self.draws
        self.matches = self.wins + self.draws + self.loses
        super().save(*args, **kwargs)

class PlayerStats(models.Model):
    player= models.ForeignKey(Player)
    goals=models.IntegerField()
    assists=models.IntegerField()
    matches=models.IntegerField()
    season=season=models.ForeignKey(Season, null=True)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# TO DO dorobić więcej statystyk
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def __str__(self):
        return "{}_{}_stats".format(self.player.firstname,self.player.lastname)


class Game(models.Model):
    Team_home= models.ForeignKey(Team,related_name="home_team")
    Goals_home= models.IntegerField()
    Team_away = models.ForeignKey(Team,related_name="away_team")
    Goals_away = models.IntegerField()
    Stadium=models.ForeignKey(Stadium,blank=True,null=True)
    competition=models.ForeignKey(Competition, related_name="competition",null=True)
    Date_game=models.DateTimeField()
    time=models.CharField(max_length=4,default="0")
    tag=models.CharField(max_length=10)
    slug=models.SlugField(allow_unicode=True)



    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["Date_game"]


class GameEvent(models.Model):
    name=models.CharField(max_length=30)
    slug=models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class GameEvents(models.Model):
    game=models.ForeignKey(Game)
    player=models.ForeignKey(Player)
    minute=models.IntegerField()
    home=models.BooleanField()
    event=models.ForeignKey(GameEvent,related_name="game_event")

    def __str__(self):
        return "{} {}".format(self.game, self.player)
