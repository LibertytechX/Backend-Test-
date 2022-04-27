from django.shortcuts import get_object_or_404
from .models import Coin, User
from .serializers import UserSerializer, CoinSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from .get_coins import CoinApi
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework import status
import requests
from .permissions import IsOwnerOrReadOnly, IsOwner


class CreateUser(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Created user successfully',
            'username': response.data['username'],
            'status': 200,
        })


class UserListAPIView(ListAPIView):
    """
    get:
        Returns list of all exisiting users
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class ListCoinsAPIView(APIView):
    # List All Coins API View
    def get(self, request, format=None):
        coin_api_instance = CoinApi()
        data = coin_api_instance.get_all_coins()
        return Response(data[:100])


class AddFavoriteCoinsAPIView(APIView):
    # View to Add Favorite Coin(s)
    def post(self, request, format=None):
        serializer_class = CoinSerializer
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        coin_name = serializer.validated_data['coin_name']
        usd_price = serializer.validated_data['usd_price']

        # Check if coin exists
        coin_instance = CoinApi()
        coin_exists = coin_instance.check_if_coin_exists(coin_name)

        if not User.objects.filter(username=username).exists():
            return Response({'message': "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        elif coin_exists == False:
            return Response({'message': "the coin you are trying to add does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if Coin.objects.filter(user__username=username, coin_name=coin_name).exists():
            return Response({'message': "Coin already added to your favourites"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        responseData = {
            'message': f'Added {coin_name} to Favourite successfully',
            'username': username,
            'coin-name': coin_name,
            'status': status.HTTP_201_CREATED,
        }

        return Response(responseData, status=status.HTTP_201_CREATED)


class FavoriteCoinsListView(APIView):
    def post(self, request, format=None):
        username = request.data['username']
        user = get_object_or_404(User, username=username)
        favourite_names = list(Coin.objects.filter(
            user_id=user.id).values_list('coin_name', flat=True))
        api_instance = CoinApi()
        result = api_instance.get_coins_for_coin_names(favourite_names)
        responseData = {
            "message": f"Welcome back {username} thanks for using our platform",
            "subscribed_favourites": result
        }
        return Response(responseData, status=status.HTTP_200_OK)
