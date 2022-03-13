from os import stat
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, FavouriteCoin
from .serializers import FavoriteCoinSerializer, UserSerializer
from .coin_api import CoinAPI


class RegisterUserView(APIView):
    def post(self, request):
        serializer_class = UserSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            responseData = {
                'message':"Created user successfully",
                'username':account.username,
                'status':status.HTTP_201_CREATED
            }

            return Response(responseData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCoinsAPIView(APIView):
    # List All Coins API View
    def get(self, request, format=None):
        coin_api_instance = CoinAPI()
        data = coin_api_instance.get_all_coins()
        return Response(data)


class AddFavoriteCoinsAPIView(APIView):
    # View to Add Favorite Coin(s)
    def post(self, request, format=None):
        serializer_class = FavoriteCoinSerializer
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        coin_name = serializer.validated_data['coin_name']

        if not User.objects.filter(username=username).exists():
            return Response({'message': "user does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if FavouriteCoin.objects.filter(user__username=username, coin_name=coin_name).exists():
            return Response({'message':"Coin already added to your favourites"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        responseData = {
            'message': f'Added {coin_name} to Favourite successfully',
            'username':username,
            'coin-name':coin_name,
            'status':status.HTTP_201_CREATED,
        }

        return Response(responseData, status=status.HTTP_201_CREATED)



class UserFavoriteCoinsListView(APIView):
    def post(self, request, format=None):
        username = request.data['username']
        user = get_object_or_404(User, username=username)
        favourite_names = list(FavouriteCoin.objects.filter(user_id=user.id).values_list('coin_name', flat=True))
        api_instance = CoinAPI()
        result = api_instance.get_coins_for_coin_names(favourite_names)
        responseData = {
            "message": f"Welcome back {username} thanks for using our platform",
            "subscribed_favourites":result
            }
        return Response(responseData, status=status.HTTP_200_OK)