from django.urls import include, path
from rest_framework import routers

from api.views import BasketModelViewSet, GameModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'games', GameModelViewSet)
router.register(r'baskets', BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
