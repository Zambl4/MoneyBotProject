import json
import requests
from config import *

#создаем свой класс для ошибок конвертации

class ExchangeException(Exception):
    pass

#создаем функцию для конвертации

class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        #проверяем принятые в функцию значения

        if quote == base:
            raise ExchangeException(f'Введены одинаковые валюты: {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'Неверная валюта: {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'Неверная валюта: {base}')

        #проверяем, что эмаунт это число

        try:
            amount = float(amount)
        except ValueError:
            raise ExchangeException(f'Неверное количество: {amount}')

        #проверка ввода эмаунта на ноль и значения ниже нуля

        if amount <= 0:
            amount = int(amount)
            raise ExchangeException(f'Неверное количество: {amount}')

        #забираем данные с апишки в джейсоне

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        print(r)

        #преобразуем джейсон в список, забираем из него нужное значение, дергаем по сокращению валюты

        total_base = float(json.loads(r.content)[keys[base]])

        total_base = total_base * amount

        return total_base
