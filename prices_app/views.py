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
    price: Union[str, None] = None


class BinanceGetPriceChangePercentSend(BaseModel):
    symbol: str


class BinanceGetPriceChangePercentResponse(BaseModel):
    symbol: str
    code: Union[int, None] = None
    msg: Union[int, None] = None
    priceChangePercent: str = None


class CoinTools:

    def __init__(self, symbol: str):
        self.symbol = symbol

    @staticmethod
    def __status_code_check(code):
        if code == 200:
            return True
        return False

    def coin_icon(self) -> Union[bytes, None, bool]:
        url = f"https://coinicons-api.vercel.app/api/icon/{self.symbol}"
        response = get(url=url)
        if not self.__status_code_check(response.status_code):
            return False
        image_encoded = b64encode(response.content)
        return image_encoded

    def coin_price(self) -> Union[str, False]:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.symbol.upper()}USDT"
        response = get(url=url)
        if not self.__status_code_check(response.status_code):
            return False
        response = BinanceGetPriceResponse(**response.json())
        if response.price is not None:
            return response.price
        return "Try agien"

    def coin_price_change_percent(self) -> Union[str, bool, None]:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        parameters = BinanceGetPriceChangePercentSend(symbol=f"{self.symbol.upper()}USDT").model_dump(mode='json')
        response = post(url=url, json=parameters)
        if not self.__status_code_check(response.status_code):
            return False
        response = BinanceGetPriceChangePercentResponse(**response.json())
        if response.priceChangePercent is not None:
            return response.priceChangePercent
        return "Try again"

    def get_coin(self):
        pass


def prices(request):
    context = {

    }
    return render(
        request=request,
        template_name='prices_app/prices_page.html',
        context=context
    )


def footer_component(request):
    return render(request, "shared/footer_component.html")


def header_component(request):
    return render(request, "shared/header_component.html")
