from django.shortcuts import render
from games.models import Game, GameGenres


def index(requests):
    context = {
        'title': 'Game Store'
    }

    return render(requests, 'games/index.html', context)


def games(requests):
    context = {
        'title': 'Game Store - Каталог',
        'games': Game.objects.all(),
        'genres': GameGenres.objects.all(),
    }

    return render(requests, 'games/games.html', context)
