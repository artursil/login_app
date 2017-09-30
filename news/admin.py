from django.contrib import admin
from . import models
# Register your models here.



admin.site.register(models.NewsPaper)
admin.site.register( models.News)
admin.site.register( models.UserViewedNews)
admin.site.register(models.NewsTags)
admin.site.register(models.NewsTeam)
