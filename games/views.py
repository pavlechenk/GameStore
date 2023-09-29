from django.shortcuts import render, HttpResponseRedirect
from games.models import Game, GameGenres, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(requests):
    context = {
        'title': 'GameStore'
    }

    return render(requests, 'games/index.html', context)


def games(requests, genre_id=None, page_number=1):
    games = Game.objects.filter(genre_id=genre_id) if genre_id else Game.objects.all()

    per_page = 3
    paginator = Paginator(games, per_page)
    games_paginator = paginator.page(page_number)

    context = {
        'title': 'GameStore - Каталог',
        'games': games_paginator,
        'genres': GameGenres.objects.all(),
    }

    return render(requests, 'games/games.html', context)


@login_required
def basket_add(requests, game_id):
    game = Game.objects.get(id=game_id)
    baskets = Basket.objects.filter(user=requests.user, game=game)

    if not baskets.exists():
        Basket.objects.create(user=requests.user, game=game, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(requests.META['HTTP_REFERER'])


@login_required
def basket_remove(requests, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(requests.META['HTTP_REFERER'])


