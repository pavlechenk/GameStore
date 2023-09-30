from django.shortcuts import HttpResponseRedirect
from games.models import Game, GameGenres, Basket
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


class IndexView(TemplateView):
    template_name = 'games/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'GameStore'
        return context


class GamesListView(ListView):
    model = Game
    template_name = 'games/games.html'
    context_object_name = 'games'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_id = self.kwargs.get('genre_id')
        return queryset.filter(genre_id=genre_id) if genre_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'GameStore - Каталог'
        context['genres'] = GameGenres.objects.all()
        return context


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


