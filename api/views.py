from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from games.models import Basket, Game, GameGenres
from games.serializers import BasketSerializer, GameSerializer, GameGenreSerializer
from orders.models import Order
from orders.serializers import OrderSerializer


class GameGenreModelViewSet(ModelViewSet):
    queryset = GameGenres.objects.all()
    serializer_class = GameGenreSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()


class GameModelViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
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
                return Response({'game_id': 'Нет игры с таким идентификатором.'}, status=status.HTTP_400_BAD_REQUEST)

            obj, is_created = Basket.create_or_update(game_id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'game_id': 'Это поле обязательное для заполнения.'}, status=status.HTTP_400_BAD_REQUEST)


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_permissions(self):
        if self.action in ('destroy',):
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            address = request.data['address']
        except KeyError:
            return Response({'detail': 'Вам необходимо указать следующие обязательные поля: first_name, last_name, '
                                       'email, address.'}, status=status.HTTP_400_BAD_REQUEST)

        baskets = Basket.objects.filter(user=self.request.user)
        if baskets.exists():
            basket_history = {
                'purchased_items': [basket.de_json() for basket in baskets],
                'total_sum': float(baskets.total_price()),
            }
            order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address,
                                         basket_history=basket_history, initiator=self.request.user)

            order_serializers = self.get_serializer(order)
            return Response(order_serializers.data, status=status.HTTP_201_CREATED)

        return Response({'detail': 'Добавьте товары в корзину перед созданием заказа.'},
                        status=status.HTTP_400_BAD_REQUEST)
