from rest_framework import fields, serializers

from games.models import Basket, Game, GameGenres


class GameGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGenres
        fields = ('id', 'name', 'description')


class GameSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='name', queryset=GameGenres.objects.all())

    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'genre')


class BasketSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    sum = fields.FloatField(required=False)
    total_price = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'game', 'quantity', 'sum', 'total_price', 'total_quantity', 'created_timestamp')
        read_only_fields = ('created_timestamp',)

    def get_total_price(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_price()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
