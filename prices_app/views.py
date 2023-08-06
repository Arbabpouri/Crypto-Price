from django.shortcuts import render
from requests import get, post

from typing import Union
from pydantic import BaseModel


# Create your views here.


class BinanceResponse(BaseModel):
    code: Union[int, None] = None
    msg: Union[str, None] = None
    symbol: Union[str, None] = None
    price: Union[float, None] = None


class PriceChangePercent(BaseModel):
    symbol: str


def status_code_check(code):
    if code == 200:
        return True
    return False


class CoinTools:

    def __init__(self, symbol: str):
        self.symbol = symbol

    def coin_icon(self) -> Union[str, None]:
        url = f"https://coinicons-api.vercel.app/api/icon/{self.symbol}"
        response = get(url=url)
        if not status_code_check(response.status_code): return False

    def coin_price(self) -> Union[float, str]:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.symbol.upper()}USDT"
        response = get(url=url)
        if not status_code_check(response.status_code): return False

    def coin_price_change_percent(self):
        url = "https://api.binance.com/api/v3/ticker/24hr"
        parameters = PriceChangePercent(symbol=f"{self.symbol.upper()}USDT").dict()
        response = post(url=url, json=parameters)
        if not status_code_check(response.status_code): return False


def prices(request):
    return render(request, 'price_app/prices_page.html')
