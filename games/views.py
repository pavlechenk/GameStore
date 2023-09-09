from django.shortcuts import render

# Create your views here.


def index(requests):
    context = {
        'title': 'Store'
    }

    return render(requests, 'games/index.html', context)


def games(requests):
    context = {
        'title': 'Store - Каталог'
    }

    return render(requests, 'games/games.html', context)