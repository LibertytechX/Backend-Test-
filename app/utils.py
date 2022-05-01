import requests

from decouple import config


# Application util manager.
class Util():
    @staticmethod
    def get_all_coins():
        """Fetch available coins from CoinAPI"""
        try:
            url = 'https://rest.coinapi.io/v1/assets'
            headers = {'X-CoinAPI-Key': config(
                'X_CoinAPI_Key', default='618D9FBA-CE44-4B44-89B1-284D80D70746', cast=str)}
            response = requests.get(url, headers=headers)

            return response
        except Exception as err:
            return str(err)
