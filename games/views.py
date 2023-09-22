from django.shortcuts import render, HttpResponseRedirect
from games.models import Game, GameGenres, Basket


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


def basket_remove(requests, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(requests.META['HTTP_REFERER'])


