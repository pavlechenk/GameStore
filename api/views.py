from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from games.models import Game
from games.serializers import GameSerializer


class GameModelViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()
