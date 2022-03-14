from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        url = 'https://rest.coinapi.io/v1/assets'
        headers = {'req-CoinAPI-Key': '4CFFEE07-9848-40B1-B744-A52226800F12'}
        req = requests.get(url, headers=headers)

        loadUrl = 'http://127.0.0.1:8000/loaddb/'
        jsonDataLength = req.json()
        for asset in jsonDataLength[100]:
            if asset.get('price_usd'):

                data = {'name': asset['asset_id'], 'price_usd': asset['price_usd'],
                        'volume': asset['volume_1mth_usd']}
                print(data)
                response = requests.post(loadUrl, data=data)

        self.stdout.write(self.style.SUCCESS('Database loaded successfully'))
