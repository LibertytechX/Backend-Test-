import requests





def get_coin_data(url):
    headers = {'X-CoinAPI-Key' : 'BBC5397D-4195-4E57-8406-0889E73A0DCC'}
    response=requests.get(url, headers=headers)
    res=response.json()
    return res