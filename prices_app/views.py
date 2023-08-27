from django.shortcuts import render
from .models import Symbol

from requests import get
from typing import Union, Any
from pydantic import BaseModel
from base64 import b64encode
from pathlib import Path
from enum import StrEnum


# Create your views here.

class CssStatusClass(StrEnum):
    PriceIncrease = "priceIncrease"
    PriceDecrease = "priceDecrease"


class BinanceGetPriceResponse(BaseModel):
    code: Union[int, None] = None
    msg: Union[str, None] = None
    symbol: Union[str, None] = None
    price: Union[str, None] = None


class BinanceGetPriceChangePercentResponse(BaseModel):
    symbol: str
    code: Union[int, None] = None
    msg: Union[int, None] = None
    priceChangePercent: Union[str, None] = None


class Coin(BaseModel):
    name: Any
    icon: Any
    price: Any
    price_status: Any
    status_class: Any
    is_popular: bool


class CoinTools:

    def __init__(self, symbol: str):
        self.symbol = symbol

    @staticmethod
    def __status_code_check(code) -> bool:
        if code == 200:
            return True
        return False

    @staticmethod
    def __get_class_status(changes: Union[int, float]) -> str:
        if changes and changes > 0:
            return CssStatusClass.PriceIncrease
        return CssStatusClass.PriceDecrease

    def __check_icon_in_db(self) -> Union[bytes, None]:
        coin_icon = Symbol.objects.filter(symbol__exact=self.symbol).first()
        if coin_icon and coin_icon.icon:
            return coin_icon.icon
        return

    def __coin_icon(self) -> Union[str, None]:
        coin_icon = self.__check_icon_in_db()
        if coin_icon:
            return coin_icon
        url = f"https://coinicons-api.vercel.app/api/icon/{self.symbol.lower()}"
        response = get(url=url)
        if not self.__status_code_check(response.status_code):
            return Path("static/images/crypto.svg").open("rb").read().decode()
        coin_icon = b64encode(response.content).decode()
        add_icon = Symbol.objects.filter(symbol__exact=self.symbol).first()
        if add_icon is None:
            add_icon = Symbol.objects.create(symbol=self.symbol, icon=coin_icon, is_popular=False)
        else:
            add_icon.icon = coin_icon
        add_icon.save()
        return coin_icon

    def __coin_price(self) -> Union[str, None]:
        url = f"https://www.binance.com/api/v3/ticker/price?symbol={self.symbol.upper()}USDT"
        response = get(url=url)
        if not self.__status_code_check(response.status_code):
            return
        response = BinanceGetPriceResponse(**response.json())
        if response.price is not None:
            return round(float(response.price), 4)
        return

    def __coin_price_change_percent(self) -> Union[str, None]:

        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={self.symbol.upper()}USDT"
        response = get(url=url)
        if not self.__status_code_check(response.status_code):
            return
        response = BinanceGetPriceChangePercentResponse(**response.json())
        if response.priceChangePercent is not None:
            try:
                return float(response.priceChangePercent)
            except Exception:
                return
        return

    def __coin_is_popular(self):
        find_coin = Symbol.objects.filter(symbol__exact=self.symbol).first()
        if find_coin:
            return find_coin.is_popular
        add_coin = Symbol.objects.create(symbol=self.symbol)
        return add_coin.is_popular

    def get_coin(self) -> Union[Coin, None]:

        coin_icon = self.__coin_icon()
        coin_price = self.__coin_price()
        coin_status = self.__coin_price_change_percent()
        coin_class_status = self.__get_class_status(coin_status)
        coin_is_popular = self.__coin_is_popular()
        coin = Coin(
            name=self.symbol,
            icon=coin_icon,
            price=coin_price,
            price_status=coin_status,
            status_class=coin_class_status,
            is_popular=coin_is_popular
        )

        return coin


def prices(request):
    symbols = Symbol.objects.all()
    coins = []
    for coin in symbols:
        coin_information = CoinTools(symbol=coin.symbol).get_coin()
        if coin_information:
            coins.append(coin_information.dict())
    context = {"coins": coins}
    return render(
        request=request,
        template_name='prices_app/prices_page.html',
        context=context
    )


def footer_component(request):
    return render(request, "shared/footer_component.html")


def header_component(request):
    return render(request, "shared/header_component.html")
