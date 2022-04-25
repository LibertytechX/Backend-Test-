from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, AllCoinsSerializer
from .models import AllCoins
from rest_framework import status
import requests


@api_view(['GET'])
def home_view(request):
    message = {
        "Message": "Hello New API"
    }
    return Response(message, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {
                    "message": "Created user successfully",
                    "username": user_serializer.data.get('name'),
                    "status": 200
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Message": "Use a post request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_coins(request):
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': 'D7E30FDE-1B4A-47DD-9496-06E215DB7EEA'}
    response = requests.get(url, headers=headers)
    new_list = []
    count = 0
    all_coins = AllCoins.objects.all()
    for data in response.json():

        new_list.append({'pk': count, 'name': data.get('asset_id'), 'USD-PRICE': data.get('price_usd'),
                        'volume': data.get('volume_1mth_usd')})
        count += 1
        if len(new_list) == 15041:
            break
    for x in new_list:
        if all_coins.count() == 15041:
            break
        else:
            AllCoins.objects.create(name=x['name'], usd_price=x['USD-PRICE'], volume=x['volume'])
    serialized_coins = AllCoinsSerializer(all_coins, many=True)
    return Response(serialized_coins.data, status=status.HTTP_200_OK)
