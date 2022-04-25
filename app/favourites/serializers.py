from rest_framework import serializers
from .models import Favourite


class FavouritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = [
            "user",
            "name",
            "usd_price",
            "volume"
        ]

