from rest_framework.test import APIClient
from rest_framework import status

from coins.models.coin_model import Coin
from django.test import TestCase
from django.urls import reverse


# Create your test(s) here.
class TestCoinAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by test method"""
        Coin.objects.create(
            name='BTC',
            usd_price='42,3529',
            volume='19,331,340'
        )
        Coin.objects.create(
            name='SAND',
            usd_price='100',
            volume='19,331,340,302'
        )
        Coin.objects.create(
            name='ETH',
            usd_price='4,356',
            volume='199,331,340'
        )

    def setUp(self):
        self.client = APIClient()

    def test_api_return_avalilable_coins(self):
        """Test available coins are returned successful"""
        response = self.client.get(
            reverse('coins'),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Coin.objects.count(), 3)
