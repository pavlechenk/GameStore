from http import HTTPStatus
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from games.models import Basket, Game
from orders.models import Order
from users.models import User


class OrderCreateViewTestCase(TestCase):
    fixtures = ['games.json', 'genres.json']

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.path = reverse('orders:order_create')
        self.data = {
            'first_name': 'Александр',
            'last_name': 'Раздымахо',
            'email': 'test@gmail.com',
            'address': 'Россия, СПб',
        }

    def test_order_create_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'GameStore - Оформление заказа')
        self.assertTemplateUsed(response, 'orders/order_create.html')

    @patch('stripe.checkout.Session.create')
    def test_order_create_post(self, mock_stripe_create):
        Basket.objects.create(user=self.user, game=Game.objects.first(), quantity=2)

        mock_stripe_create.return_value.url = 'https://example.com/payment/checkout'

        self.assertFalse(Order.objects.filter(initiator=self.user, status=0).exists())

        self.client.post(self.path, self.data, follow=True)

        # Проверяю, что создался сеанс оплаты и заказ
        self.assertTrue(mock_stripe_create.called)
        self.assertTrue(Order.objects.filter(initiator=self.user, status=0).exists())
