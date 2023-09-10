from django.contrib import admin
from games.models import GameGenres, Game


admin.site.register(GameGenres)
admin.site.register(Game)
