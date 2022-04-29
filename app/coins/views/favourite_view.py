from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status

from core.models import User
from coins.models.coin_model import Coin
from coins.models.favourite_model import FavouriteCoin
from coins.serializers.favourite_serializer import (
    ViewFavouriteSerializer, AddFavouriteSerializer
)
from lib.response import Response


# Create your view(s) here.
class ViewFavouriteAPIView(ListAPIView):
    serializer_class = ViewFavouriteSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            try:
                User.objects.get(username=username)
                favourites = FavouriteCoin.objects.filter(
                    username=username).values_list('coin')

                coins = [coin[0] for coin in favourites]
                subscribed_favourites = list(Coin.objects.filter(pk__in=coins).values(
                    'name', 'usd_price', 'volume'))

                return Response(data={
                    'message': f'Welcome back {username}, thanks for using our platforrm',
                    'subscribed_favourites': subscribed_favourites,
                }, status=status.HTTP_200_OK)

            except User.DoesNotExist as err:
                return Response(errors={
                    'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)


class AddFavouriteAPIView(CreateAPIView):
    serializer_class = AddFavouriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            favourite = serializer.validated_data['favourite']
            try:
                User.objects.get(username=username)
                coin = Coin.objects.get(name=favourite)
                favourite_coin = FavouriteCoin.objects.filter(
                    username=username).values_list('favourite')

                for coins in favourite_coin:
                    if favourite in coins:
                        return Response(errors={
                            'error': 'Favourite already exist'},
                            status=status.HTTP_400_BAD_REQUEST)

                serializer.save(coin=coin)

                return Response(data={
                    'message': f'Added {favourite} to Favourite successfully',
                    'username': username,
                    'coin_name': favourite,
                }, status=status.HTTP_200_OK)

            except (User.DoesNotExist, Coin.DoesNotExist) as err:
                return Response(errors={'error': str(err)},
                                status=status.HTTP_400_BAD_REQUEST)
