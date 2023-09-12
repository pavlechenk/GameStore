from django.urls import path
from games.views import games

app_name = 'games'

urlpatterns = [
    path('', games, name='index'),
]
