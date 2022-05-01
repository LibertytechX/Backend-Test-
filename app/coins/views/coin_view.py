from rest_framework.generics import ListAPIView
from rest_framework import status

from utils import Util
from coins.serializers.coin_serializer import CoinSerializer
from lib.response import Response


# Create your view(s) here.
class CoinAPIView(ListAPIView):
    serializer_class = CoinSerializer

    def list(self, request):
        """Return a list of available coins"""
        try:
            coins = []
            response = Util.get_all_coins()

            for data in response.json():
                coins.append(
                    {
                        'name': data.get('asset_id'),
                        'USD-PRICE': data.get('price_usd'),
                        'volume': data.get('volume_1hrs_usd')
                    })

                if len(coins) == 3:
                    break
            return Response(data={'coins': coins}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(errors={'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
