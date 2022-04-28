from rest_framework import viewsets
from .serializer import UserSerializer, CoinSerializer
from rest_framework import status
from rest_framework.views  import APIView
from rest_framework.response import Response
import requests, json
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .models import Coin, User



class UserClass(APIView):

    def post(self, request):
        serializer_request = UserSerializer(data = request.data)
        if serializer_request.is_valid():
            serializer_request.save()
            res = {
                "message":"created user Successfully",
                "username": serializer_request.data["username"],
                "status-code": 200
            }

            return Response(res,status = status.HTTP_201_CREATED)
        return Response(serializer_request.errors, status = status.HTTP_400_BAD_REQUEST)


class CoinClass(APIView):

    def get(self,request):
        coins = Coin.objects.all()
        all_coins = CoinSerializer(coins,many = True)
        return Response(all_coins.data, status = status.HTTP_200_OK)




@api_view(["POST"])
def add_favourite(request):
    try:
        if request.data.get("username"):

           user = get_object_or_404(User,username = request.data["username"])
        else:
            res = {"error": "Missing Field Username"}
            return Response(res,status= status.HTTP_404_NOT_FOUND)
            
        try:
            if request.data.get("favourite"):
                
                coin = get_object_or_404(Coin,name = request.data["favourite"])
                current_coins =  user.favourite_coins
                
                user.favourite_coins.append(coin.name)
                print(user.favourite_coins)
                user.save()
                res = {"message": f"Added {coin.name}  Favourite Successfully ",
                    "username" : user.username,
                    "coin-name" : coin.name,
                    "status-code": 200
                    }
                return Response(res,status= status.HTTP_201_CREATED)
            else:
                res = {"error": "Missing Field Favourite Name"}
                return Response(res,status= status.HTTP_404_NOT_FOUND)
            

        except Coin.DoesNotExist:
            res = {"error": "Coin does not  exist"}
            return Response(res,status= status.HTTP_404_NOT_FOUND)

    except Coin.DoesNotExist:
        res = {"error": "User does not exist"}
        return Response(res,status= status.HTTP_404_NOT_FOUND)
    






@api_view(["GET"])
def view_favourite(request):
    try:
        if request.data.get("username"):
            user = get_object_or_404(User,username = request.data["username"])
        else:
            res = {"error": "Missing Field Username"}
            return Response(res,status= status.HTTP_404_NOT_FOUND)
            
        try:
            favourite_coins_names = user.favourite_coins
            coins = Coin.objects.filter(name__in= favourite_coins_names)
            fav_coins = CoinSerializer(coins, many = True)
            res = {"message": f"Welcome  back {user.username}  thanks for using our platform",
                  "subscribed_favourites" : fav_coins.data
                  }
            return Response(res,status= status.HTTP_200_OK)

        except Exception as e:
            res = {"error": "Fail to fetch records"}
            return Response(res,status= HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Coin.DoesNotExist:
        res = {"error": "User does not exist"}
        return Response(res,status= status.HTTP_404_NOT_FOUND)
    
    
    






