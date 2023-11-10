import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class GameGenres(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'GameGenre'
        verbose_name_plural = 'GameGenres'

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='games_images', null=True, blank=True)
    stripe_game_price_id = models.CharField(max_length=128, null=True, blank=True)
    genre = models.ForeignKey(to=GameGenres, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

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
    def total_price(self):
        return sum([basket.sum() for basket in self])

    def total_quantity(self):
        return sum([basket.quantity for basket in self])

    def stripe_games(self):
        return [{'price': basket.game.stripe_game_price_id, 'quantity': basket.quantity} for basket in self]


def basket_add(game_id, user):
    game = Game.objects.get(id=game_id)
    baskets = Basket.objects.filter(user=user, game=game)

    if not baskets.exists():
        Basket.objects.create(user=user, game=game, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт: {self.game.name}"

    def sum(self):
        return self.game.price * self.quantity

    def de_json(self):
        baskets_item = {
            'game_name': self.game.name,
            'quantity': self.quantity,
            'price': float(self.game.price),
            'sum': float(self.sum()),
        }

        return baskets_item

    @staticmethod
    def create_or_update(game_id, user):
        baskets = Basket.objects.filter(user=user, game_id=game_id)

        if not baskets.exists():
            obj = Basket.objects.create(user=user, game_id=game_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created
