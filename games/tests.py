from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from games.models import Game, GameGenres


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'GameStore')
        self.assertTemplateUsed(response, 'games/index.html')


class GamesListViewTestCase(TestCase):
    fixtures = ['games.json', 'genres.json']

    def setUp(self):
        self.games = Game.objects.all()

    def test_list(self):
        path = reverse('games:index')
        response = self.client.get(path)

        self.__common_test(response)
        self.assertEqual(list(response.context_data['games']), list(self.games[:3]))

    def test_list_with_category(self):
        genre = GameGenres.objects.first()
        path = reverse('games:genre', kwargs={'genre_id': genre.id})
        response = self.client.get(path)

        self.__common_test(response)
        self.assertEqual(
            list(response.context_data['games']),
            list(self.games.filter(genre_id=genre.id))
        )

    def __common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'GameStore - Каталог')
        self.assertTemplateUsed(response, 'games/games.html')
