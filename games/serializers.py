from rest_framework import serializers

from games.models import Game, GameGenres


class GameSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='name', queryset=GameGenres.objects.all())

    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'genre')
