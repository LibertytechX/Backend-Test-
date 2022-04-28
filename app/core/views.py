from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FavouritesSerializer, UserSerializer, AllCoinsSerializer
from .models import AllCoins, Favourite, User
from rest_framework import status
import requests

# Register users

@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            # Response message
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
    # Get all coins from coinapi
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': 'B0853F54-F9C3-4AA3-B1BB-16B909E7CBEF'}
    response = requests.get(url, headers=headers)
    new_list = [] # Create a new list to store the data
    count = 0
    all_coins = AllCoins.objects.all()
    for data in response.json():

        new_list.append({'pk': count, 'name': data.get('asset_id'), 'USD-PRICE': data.get('price_usd'),
                        'volume': data.get('volume_1mth_usd')})
        count += 1
        if len(new_list) == 2000:
            break
    for x in new_list:
        if all_coins.count() == 2000:
            break
        else:
            AllCoins.objects.create(name=x['name'], usd_price=x['USD-PRICE'], volume=x['volume'])
    serialized_coins = AllCoinsSerializer(all_coins, many=True)
    return Response(serialized_coins.data, status=status.HTTP_200_OK)

# View all favourites
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

# Add favourites
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