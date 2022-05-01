from coins.models.coin_model import Coin
from coins.models.favourite_model import FavouriteCoin

from django.test import TestCase


# Create your test(s) here.
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        coin = Coin.objects.create(
            name='ETH',
            usd_price='4,356',
            volume='199,331,340')

        FavouriteCoin.objects.create(
            coin=coin,
            username='way2teiker',
            favourite='ETH')

    def test_coin_create_successful(self):
        """Test Coin is created successful"""
        coin = Coin.objects.all().values('name')[0]['name']
        self.assertEqual(coin, 'ETH')
        self.assertEqual(Coin.objects.count(), 1)

    def test_favourite_create_successful(self):
        """Test Favourite is created successful"""
        favourite = FavouriteCoin.objects.all().values(
            'favourite')[0]['favourite']

        self.assertEqual(favourite, 'ETH')
        self.assertEqual(FavouriteCoin.objects.count(), 1)
