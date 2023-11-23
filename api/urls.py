from django.urls import include, path
from rest_framework import routers

from api.views import (BasketModelViewSet, GameModelViewSet, OrderModelViewSet,
                       GameGenreModelViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'games', GameModelViewSet)
router.register(r'baskets', BasketModelViewSet)
router.register(r'orders', OrderModelViewSet)
router.register(r'genres', GameGenreModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
