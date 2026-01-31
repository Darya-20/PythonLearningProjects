import requests
import json
import xmltodict
from config import keys, API_KEY

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}.')
    
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
    
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
    
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        
        
        total_base = ExchangeRateAPI.get_price(base, quote, amount)
        return total_base
        
        
class ExchangeRateAPI:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{keys[base]}")
        data = response.json()

        exchange_rate = data['conversion_rates'][keys[quote]]
        total_base = exchange_rate * amount
        return total_base
