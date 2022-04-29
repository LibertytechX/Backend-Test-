import os
import json
from ntpath import join
import requests
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view
from dotenv import load_dotenv
load_dotenv()
COIN_API = os.getenv('COIN_API')
from core.models import User, FavCoin

@api_view(['POST'])
def register(req) -> Response: 

    try:
        data = json.loads(req.body)
        new_user = User.objects.create_user(data['email'], password=data['password'])
        new_user.name = data['username']
        new_user.save()
        res_body = {
            "message": "Created user successfully",
            "username": new_user.name,
            "status-code": 200
        }
        return Response(res_body,
        status=status.HTTP_200_OK)
    except json.decoder.JSONDecodeError as err:
        return Response({'detail': 'Unable to process payload body'},
        status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_all_coins(req) -> Response: 
    url = 'https://rest.coinapi.io/v1/assets'
    json = get_coin_api(url)
    price_list = []
    for asset in json:
        price = round(asset.get('price_usd', 0))
        volume = round(asset['volume_1hrs_usd'])
        price_list.append({
            "name": asset['asset_id'], 
            "USD_PRICE": f"{price:,}",
            "volume": f"{volume:,}"
        })
    return Response(price_list,
        status=status.HTTP_200_OK)


@api_view(['POST'])
def add_favorite(req) -> Response:
    url = 'https://rest.coinapi.io/v1/assets'
    try:
        data = json.loads(req.body)
        user = User.objects.get(name=data['username'])


        res = get_coin_api(f"{url}/{data['favourite']}")
        asset = res[0]
        fav, created = FavCoin.objects.get_or_create(username=user.name, coin_name=data['favourite'])
        if not created:
            return Response({"detail": f"{fav.coin_name} has already been added"},
        status=status.HTTP_400_BAD_REQUEST)
        price = round(asset.get('price_usd', 0))
        volume = round(asset['volume_1hrs_usd'])
        fav.usd_price=f"{price:,}"
        fav.volume=f"{volume:,}"
        fav.save() 
        res_body = {
            "message": "Added USDT to Favourite successfully",
            "username": "way2teiker",
            "coin-name": "USDT",
            "status-code": 200
        }
        return Response(res_body,
        status=status.HTTP_200_OK)
    except User.DoesNotExist as err:
         return Response({'detail': 'username not found'},
         status=status.HTTP_404_NOT_FOUND)
    except json.decoder.JSONDecodeError as err:
        return Response({'detail': 'Unable to process payload body'},
        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def view_favorites(req) -> Response:
    try:
        data = json.loads(req.body)
        sub_favs = FavCoin.objects.filter(username=data['username'])
        return format_favs(sub_favs)
    except json.decoder.JSONDecodeError as err:
        return Response({'detail': 'Unable to process payload body'},
        status=status.HTTP_400_BAD_REQUEST)


def format_favs(subcribed_favs) -> Response:
    fav_list = []
    res_boy = {
        "message": "Welcome back way2teiker thanks for using our platform",
        "subscribed_favourites": fav_list
    }
    for sub in subcribed_favs:
        fav_list.append({
            "name": sub.coin_name,
            "USD-PRICE": sub.usd_price,
            "volume": sub.volume
        })
    return Response(res_boy, status=status.HTTP_200_OK)

def get_coin_api(url):
    headers = {'X-CoinAPI-Key' : COIN_API}
    response = requests.get(url, headers=headers)
    json = response.json()
    return json
