from django.shortcuts import render
from requests import get, post
from typing import Union
from pydantic import BaseModel
from base64 import b64encode


# Create your views here.


class BinanceGetPriceResponse(BaseModel):
    code: Union[int, None] = None
    msg: Union[str, None] = None
    symbol: Union[str, None] = None
    price: Union[float, None] = None


class BinanceGetPriceChangePercentSend(BaseModel):
    symbol: str


class BinanceGetPriceChangePercentResponse(BinanceGetPriceChangePercentSend):
    code: Union[int, None] = None
    msg: Union[int, None] = None
    priceChangePercent: str = None


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
        image_encoded = b64encode(response.content)
        return image_encoded

    def coin_price(self) -> str:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.symbol.upper()}USDT"
        response = get(url=url)
        if not status_code_check(response.status_code): return False
        response = BinanceGetPriceResponse(**response)
        if response.price is not None:
            return response.price
        return "Try agien"

    def coin_price_change_percent(self):
        url = "https://api.binance.com/api/v3/ticker/24hr"
        parameters = BinanceGetPriceChangePercentSend(symbol=f"{self.symbol.upper()}USDT").dict()
        response = post(url=url, json=parameters)
        if not status_code_check(response.status_code): return False
        response = BinanceGetPriceChangePercentResponse(**response.json())
        if response.priceChangePercent is not None:
            return response.priceChangePercent
        return "Try agien"


def prices(request):
    context = {

    }
    return render(
        request=request,
        template_name='price_app/prices_page.html',
        context=context
    )
