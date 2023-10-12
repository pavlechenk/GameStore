import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class GameGenres(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='games_images')
    stripe_game_price_id = models.CharField(max_length=128, null=True, blank=True)
    genre = models.ForeignKey(to=GameGenres, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_game_price_id:
            stripe_game_price = self.get_stripe_game_price()
            self.stripe_game_price_id = stripe_game_price['id']
        super().save(force_insert, force_update, using, update_fields)

    def get_stripe_game_price(self):
        stripe_game = stripe.Product.create(name=self.name)
        stripe_game_price = stripe.Price.create(
            product=stripe_game['id'], unit_amount=round(self.price * 100), currency='rub')
        return stripe_game_price

    def __str__(self):
        return f"Игра: {self.name} | Жанр: {self.genre}"


class BasketQuerySet(models.QuerySet):
    def get_total_price(self):
        return sum([basket.get_price() for basket in self])

    def get_total_quantity(self):
        return sum([basket.quantity for basket in self])

    def stripe_games(self):
        return [{'price': basket.game.stripe_game_price_id, 'quantity': basket.quantity} for basket in self]


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт: {self.game.name}"

    def get_price(self):
        return self.game.price * self.quantity

    def de_json(self):
        baskets_item = {
            'game_name': self.game.name,
            'quantity': self.quantity,
            'price': float(self.game.price),
            'sum': float(self.get_price()),
        }

        return baskets_item
