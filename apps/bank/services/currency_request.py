import requests
from bank.models import ExchangeRate

def crate_exchange_currency(api_key: str, 
                            base_currency: str, 
                            target_currencies: list):
    url = f'https://open.er-api.com/v6/latest/{base_currency}'
    params = {'apikey': api_key}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        rates = data['rates']

        for target_currency in target_currencies:
            rate = 1 / rates.get(target_currency)
            ExchangeRate.objects.create(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=rate
            )
    else:
        print('Не удалось получить курсы валюты.')

