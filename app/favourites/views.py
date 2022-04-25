from django.shortcuts import render
from rest_framework import status 
from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from .models import Favourite
from .serializers import FavouritesSerializer
from core.models import User, AllCoins


@api_view(['GET'])
def view_favourites(request, name):
    try:
        user = User.objects.get(name=name)
        favourites = Favourite.objects.filter(user=user.id)
        serialized_favourites = FavouritesSerializer(favourites, many=True)
        return Response({"message": f"Welcome back {user.name} thanks for using our platform", 
                        "subscribed_favourites": serialized_favourites.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": f"This error ({e}) occured"}) 


@api_view(['POST'])
def add_favourite(request, name):
    try:
        user = User.objects.get(name=name)
        data = request.data
        data['user'] = user.id
        filtered_coin = AllCoins.objects.get(name=data.get('name'))
        
        if filtered_coin:
            data['usd_price'] = filtered_coin.usd_price
            data['volume'] = filtered_coin.volume 
            serialzed_favourite = FavouritesSerializer(data=data)
            if serialzed_favourite.is_valid():
                serialzed_favourite.save()
                message = {
                    "message": f"Added {serialzed_favourite.data.get('name')} to your favourites",
                    "username": f"{name}",
                    "coin-name": f"{serialzed_favourite.data.get('name')}",
                    "status-code": 200
                }
                return Response (message, status=status.HTTP_200_OK)
            else:
                return Response(serialzed_favourite.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": f"Sorry the coin with name {filtered_coin.name} does not exist"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": f"This error ({e}) occured"}) 
