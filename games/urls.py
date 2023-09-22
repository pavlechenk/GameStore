from django.urls import path
from games.views import games, basket_add, basket_remove

app_name = 'games'

urlpatterns = [
    path('', games, name='index'),
    path('baskets/add/<int:game_id>', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>', basket_remove, name='basket_remove'),
]
