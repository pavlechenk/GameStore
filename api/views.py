from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from games.models import Basket, Game
from games.serializers import BasketSerializer, GameSerializer


class GameModelViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            game_id = request.data['game_id']
            games = Game.objects.filter(id=game_id)
            if not games.exists():
                return Response({'game_id': 'There is no game with this ID.'}, status=status.HTTP_400_BAD_REQUEST)

            obj, is_created = Basket.create_or_update(game_id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'game_id': 'This fields is required'}, status=status.HTTP_400_BAD_REQUEST)
