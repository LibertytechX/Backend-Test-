"""Implement seperation of concerns to ensure views.py only handles the views and does not call external apis."""

from django.conf import settings
import requests


class CoinAPI():
    def __init__(self):
        self.headers = {'X-CoinAPI-Key' : settings.COIN_API_KEY}
        self.base_url = 'https://rest.coinapi.io/v1/assets'
    
    
    def clean_data(self, coin_list):
        # Takes in API response and returns processed coin data
        cleaned_data = []
        for coin in coin_list:
            changedKeys =  {
                'asset_id': coin['asset_id'],
                'name': coin['name'],
                'USD-PRICE': coin.get('price_usd', None),
                'volume': coin['volume_1hrs_usd']
            }
            cleaned_data.append(changedKeys)
        return cleaned_data

    def get_all_coins(self):
        # Get all coins from API
        response = requests.get(self.base_url, headers=self.headers).json()
        return self.clean_data(response)


    def get_coins_for_coin_names(self, coin_names):
        # Get all coins for given coin names

        filter_str = '?filter_asset_id=' + ','.join(coin_names)
        url = self.base_url + filter_str
        response = requests.get(url, headers=self.headers).json()
        return self.clean_data(response)