from django.urls import path
from games.views import GamesListView, basket_add, basket_remove

app_name = 'games'

urlpatterns = [
    path('', GamesListView.as_view(), name='index'),
    path('genre/<int:genre_id>', GamesListView.as_view(), name='genre'),
    path('page/<int:page>', GamesListView.as_view(), name='paginator'),
    path('baskets/add/<int:game_id>', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>', basket_remove, name='basket_remove'),
]
