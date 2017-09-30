from django.contrib import auth
from django.db import models
from django.utils import timezone
from tags.models import Team, Tags , League


class User(auth.models.User, auth.models.PermissionsMixin):
    pass
    # def __str__(self):
    #     return "@{}".format(self.username)




class UserProfile(models.Model):


    UserProfile = models.OneToOneField(auth.models.User,default=1)
    fav_team = models.ForeignKey(Team,default=1,related_name='favteams')
    tags=models.ManyToManyField(Tags,through='UserTags')

    def __str__(self):
        return "{}".format(self.UserProfile)

class UserTags(models.Model):
    user=models.ForeignKey(UserProfile,related_name="usertags")
    tag=models.ForeignKey(Tags)
    negative=models.BooleanField(default=False)

    def __str__(self):
        return "{}_{}".format(self.user,self.tag.pk)

    class Meta:
        unique_together = ("tag", "user")
