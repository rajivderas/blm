from django.contrib import admin

from .models import Game, PlayerStat, TeamStat

# Register your models here.
models = [Game,TeamStat,PlayerStat]
admin.site.register(models)
