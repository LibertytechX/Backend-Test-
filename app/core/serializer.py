from rest_framework import serializers

from .models import User, Coin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'is_staff','is_superuser')


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('name','USD_PRICE','volume')

    