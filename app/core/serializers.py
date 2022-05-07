from builtins import len
from .models import User, Coin, Favourite
from rest_framework import serializers
from django.conf import settings

ADD_COIN_ACTION = settings.ADD_COIN_ACTION


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=224, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            full_name=validated_data['full_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    message = serializers.CharField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['full_name',
                  ]


class AssetsListSerializer(serializers.Serializer):
    name = serializers.CharField()
    volume = serializers.CharField()

    def get_name(self, obj):
        return obj.name

    def get_volume(self, obj):
        return obj.volume


class CoinSerializer(serializers.ModelSerializer):
    class Meta():
        model = Coin
        fields = ['name']


class AddCoinActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ADD_COIN_ACTION:
            raise serializers.ValidationError("this is not a valid action to coin")
        return value


class AddCoinSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = ProfileSerializer(source='User', read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Coin
        fields = ['user', 'id', 'name', ]

    def get_name(self, obj):
        return obj.name

    def get_id(self, obj):
        return obj.id

    def get_id(self, obj):
        return obj.id


class AddViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = ProfileSerializer(source='User', read_only=True)
    coin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Favourite
        fields = ['user', 'id', 'coin']

    def get_coin(self, obj):
        return obj.name

    def get_user(self, obj):
        return obj.full_name
