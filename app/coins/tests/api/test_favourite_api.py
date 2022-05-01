from rest_framework.test import APIClient
from rest_framework import status

from coins.models.coin_model import Coin
from coins.models.favourite_model import FavouriteCoin

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


# Create your test(s) here.
class TestFavouriteAPI(TestCase):
    def setUp(self):
        """
        Set up server client and required objects 
        for checks.
        """
        self.client = APIClient()

        get_user_model().objects.create(
            email='teiker@libertymail.com',
            username='way2teiker',
            password='Solarizedgowns')

        Coin.objects.create(
            name='USDT',
            usd_price='47,3567',
            volume='179,371,370')

    def test_api_add_favourite_coins_to_username(self):
        """Test favourite coins add to username"""
        data = {
            'coin': Coin.objects.get().id,
            'username': 'way2teiker',
            'favourite': 'USDT'}

        response = self.client.post(
            reverse('add-favourites'),
            data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FavouriteCoin.objects.count(), 1)

    def test_api_username_field_may_not_be_blank(self):
        """Test username as required field"""
        data = {
            'coin': Coin.objects.get().id,
            'username': '',
            'favourite': 'USDT'}

        response = self.client.post(
            reverse('add-favourites'),
            data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FavouriteCoin.objects.count(), 0)

    def test_api_favourite_field_may_not_be_blank(self):
        """Test favourite as required field"""
        data = {
            'coin': Coin.objects.get().id,
            'username': 'way2teiker',
            'favourite': ''}

        response = self.client.post(
            reverse('add-favourites'),
            data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FavouriteCoin.objects.count(), 0)
