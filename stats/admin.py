from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Stadium)
admin.site.register(models.Player)
admin.site.register(models.PlayerStats)
admin.site.register(models.Game)
admin.site.register(models.TeamStats)
admin.site.register(models.GameEvent)
admin.site.register(models.GameEvents)
admin.site.register(models.Competition)
admin.site.register(models.Season)
