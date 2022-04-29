import requests

from decouple import config
from rest_framework.generics import ListAPIView
from rest_framework import status

from coins.models.coin_model import Coin
from coins.serializers.coin_serializer import CoinSerializer
from lib.response import Response


# Create your view(s) here.
class CoinAPIView(ListAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer

    def list(self, request):
        """Return a list of available coins"""
        try:
            url = 'https://rest.coinapi.io/v1/assets'
            headers = {'X-CoinAPI-Key': config(
                'X_CoinAPI_Key', default='618D9FBA-CE44-4B44-89B1-284D80D70746', cast=str)}
            response = requests.get(url, headers=headers)

            get_all_coins = []

            for data in response.json():
                get_all_coins.append(
                    {
                        'name': data.get('asset_id'),
                        'USD-PRICE': data.get('price_usd'),
                        'volume': data.get('volume_1hrs_usd')
                    })

                if len(get_all_coins) == 3:
                    break
            return Response(data={'coins': get_all_coins}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(errors={'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
