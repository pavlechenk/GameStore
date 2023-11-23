from rest_framework import serializers

from djoser.serializers import UserSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    initiator = UserSerializer()

    class Meta:
        model = Order
        fields = ('id', 'first_name', 'last_name', 'email', 'address', 'basket_history', 'created', 'initiator',
                  'status')
        read_only_fields = ('created',)
