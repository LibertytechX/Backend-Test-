from django.core.management.base import BaseCommand
from core.models import Coins
import requests




class Command(BaseCommand):
    help = '''Populates the db with data from 'https://rest.coinapi.io/v1/assets'. '''

    def handle(self, *args, **kwargs):
        url = 'https://rest.coinapi.io/v1/assets'
        headers = {'X-CoinAPI-Key' : '834FC39D-7229-4E8B-BDF0-9E95988CF23C'}
        x = requests.get(url, headers=headers)

        url2 = 'http://127.0.0.1:8000/loaddb/'

        for asset in x.json()[:50]:
            if asset.get('price_usd'):
              
                data = {'name': asset['asset_id'], 'price_usd': asset['price_usd'], 'volume': asset['volume_1mth_usd']}
                # print(data)
                response = requests.post(url2, data=data)
                

        self.stdout.write(self.style.SUCCESS('Database loaded successfully'))
        
