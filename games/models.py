from django.db import models
from users.models import User


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
    genre = models.ForeignKey(to=GameGenres, on_delete=models.CASCADE)

    def __str__(self):
        return f"Игра: {self.name} | Жанр: {self.genre}"


class BasketQuerySet(models.QuerySet):
    def get_total_price(self):
        return sum([basket.get_price() for basket in self])

    def get_total_quantity(self):
        return sum([basket.quantity for basket in self])


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



