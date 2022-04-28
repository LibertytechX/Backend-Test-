from django.core.management.base import BaseCommand
import requests
from core.models import Coin

class Command(BaseCommand):

    def handle(self, *args, **options):
        api_key = '3193135D-3236-4E04-AA50-83051B3FD743'
        url = 'https://rest.coinapi.io/v1/assets'

        help = "Get all coins details from coinapi"


        headers = {'X-CoinAPI-Key' : api_key}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = []
                for coin in response.json():
                    res = {"name":coin.get("asset_id") ,"USD_PRICE":coin.get("price_usd"),"volume":coin.get("volume_1mth_usd")} 
                    coin_info = Coin(name = coin.get("asset_id"), USD_PRICE= coin.get("price_usd"), volume = coin.get("volume_1mth_usd"))
                    coin_info.save()
                print("All Records inserted into the Database")
            else:
                    res = {"error": f"Failed to fetch data with error {response.json()}" }

        except Exception as e:
            
            res = {"error": f"Failed to fetch data with error {e}" }
            print(res)

            

