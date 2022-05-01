from rest_framework import serializers

from coins.models.coin_model import Coin


# Create your serializer(s) here.
class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['name', 'usd_price', 'volume']
