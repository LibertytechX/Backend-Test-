from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Coin, Favourite
from .serializers import UserRegisterSerializer, CoinSerializer, FavouriteCreateSerializer, FavouriteSerializer
from rest_framework.permissions import IsAuthenticated
from .utils import get_coin_data
from django.http import HttpResponse
from rest_framework.decorators import api_view

class RegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            return Response({
                    "message": "Created user successfully",
                    "username" : user_data.get("name"), 
                    "status_code" : status.HTTP_200_OK}, status=status.HTTP_201_CREATED)
        return Response({
                         "error":serializer.errors,
                        "message": "An error occur, please try again"}, 
                           status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def upload_data_view(request):
    try:
        url='https://rest.coinapi.io/v1/assets/'
        coin_details = get_coin_data(url)
        for coin in coin_details:
            
            dbcoin={
                "name":coin['asset_id'],
                "price":coin.get('price_usd', " "),
                "volume":coin['volume_1day_usd']
            }
            print(dbcoin)
            Coin.objects.create(name=dbcoin['name'], USD_PRICE=dbcoin['price'], volume=dbcoin['volume'])
    except ValueError:
        return Response(("Rubbish"))
    return Response({"data": coin_details}, status=status.HTTP_200_OK)


    


class ListAndCreateCoinApiView(ListCreateAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer


class AddFavouriteView(GenericAPIView):
    serializer_class=FavouriteCreateSerializer
    def post(self, request, *args, **kwargs):
        data=request.data
        serializer=self.serializer_class(data=data)
        serializer.is_valid()
        result=serializer.save()
        return Response(
            {"message":f"Added {result['coin-name']} to Favourite successfully",
            "username": result['username'],    
            "coin-name": result['coin-name'],
            "status_code" : status.HTTP_200_OK }, status=status.HTTP_201_CREATED 
        )


class GetMyFavouriteView(GenericAPIView):
    serializer_class=FavouriteSerializer
    def post(self, request):
         username=request.data.get('username')
         myfavourite=Favourite.objects.filter(username__name=username)
         serializer=self.serializer_class(myfavourite, many=True)
         payload=serializer.data
         return Response({
            "message": f"Welcome back {username} thanks for using our platform",
            "subscribed_favourites":payload
         }, status=status.HTTP_200_OK)






