from rest_framework import serializers
from . models import User, Coin, Favourite

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']


    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email', 'name']


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ["name", "USD_PRICE", "volume"]

class FavouriteCreateSerializer(serializers.Serializer):
    coin_id=serializers.IntegerField(write_only=True)
    username=serializers.CharField(max_length=100)

    def validate(self, attrs):
        name=attrs.get('username')
        if not User.objects.get(name=name):
            raise ValueError("there is no user with that name")

        return attrs


    def create(self, validated_data):
        coin_id=validated_data['coin_id']
        name=validated_data['username']
        coin=Coin.objects.get(id=coin_id)
        user=User.objects.get(name=name)
        if user:
            like=Favourite.objects.create(username=user)
            like.favourite.add(coin)
            payload={
                "username":user.name,
                "coin-name": coin.name
            }
        return payload


class FavouriteSerializer(serializers.ModelSerializer):
    favourite_coins=serializers.SerializerMethodField(method_name="get_favourite_coin")
    class Meta:
        model=Favourite
        fields=["favourite_coins"]

    def get_favourite_coin(self, obj):

        return CoinSerializer(obj.favourite.all(), many=True).data





        

    
