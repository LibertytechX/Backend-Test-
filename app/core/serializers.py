from rest_framework import serializers
from .models import User, Coins, Favourite



class CoinsSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Coins
        fields = ['name', 'price_usd', 'volume']


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ['user', 'favourite']
        

class SubscribedFavouritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ['favourite']
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    
    subscribed_favourites = SubscribedFavouritesSerializer(many=True, read_only=True, )
        
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'subscribed_favourites', ]
        extra_kwargs = {'password': {'write_only': True}
        }
 
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
