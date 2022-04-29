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
        """Return a list of available coin"""
        coins = self.get_queryset()
        serializer = self.get_serializer(coins, many=True)
        return Response(
            data=dict(coins=serializer.data, total=len(serializer.data)),
            status=status.HTTP_200_OK)
