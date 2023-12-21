from games.models import GameGenres


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class GameContextMixin:
    genres = GameGenres.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        genre_id = self.kwargs.get('genre_id')
        context['genres'] = self.genres
        context['current_genre'] = GameGenres.objects.get(pk=genre_id) if genre_id else None
        return context
