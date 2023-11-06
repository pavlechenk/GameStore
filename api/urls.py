from django.urls import include, path
from rest_framework import routers

from api.views import GameModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'games', GameModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
