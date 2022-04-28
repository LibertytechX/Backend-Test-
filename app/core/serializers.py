from rest_framework import serializers
from .models import User, AllCoins, Favourite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            user.save()
            return user


class AllCoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllCoins
        fields = ['name', 'usd_price', 'volume']


class FavouritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = [
            "user",
            "name",
            "usd_price",
            "volume"
        ]