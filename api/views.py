from rest_framework.viewsets import ModelViewSet

from games.models import Game
from games.serializers import GameSerializer


class GameModelViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
