from django.contrib import admin

from games.models import Basket, Game, GameGenres


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'genre')
    fields = ('name', 'description', ('price', 'quantity'), 'stripe_game_price_id', 'image', 'genre')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(GameGenres)
class GameGenresAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('game', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
