from rest_framework import serializers
from .models import User, FavouriteCoin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class FavoriteCoinSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, write_only=True)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    favourite = serializers.CharField(source='coin_name')

    class Meta:
        model = FavouriteCoin
        fields = ['user', 'username', 'favourite']

    def create(self, validated_data):
        user = User.objects.get(username=self.validated_data['username'])
        return FavouriteCoin.objects.create(user_id=user.id, coin_name=self.validated_data['coin_name'])
