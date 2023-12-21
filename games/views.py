from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import GameContextMixin, TitleMixin
from games.models import Basket, Game


class IndexView(TitleMixin, TemplateView):
    template_name = 'games/index.html'
    title = 'GameStore'


class GamesListView(TitleMixin, GameContextMixin, ListView):
    model = Game
    template_name = 'games/games.html'
    context_object_name = 'games'
    paginate_by = 3
    title = 'GameStore - Каталог'

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_id = self.kwargs.get('genre_id')
        return queryset.filter(genre_id=genre_id) if genre_id else queryset


@login_required
def basket_add(requests, game_id):
    Basket.create_or_update(game_id, requests.user)
    return HttpResponseRedirect(requests.META['HTTP_REFERER'])


@login_required
def basket_remove(requests, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(requests.META['HTTP_REFERER'])
