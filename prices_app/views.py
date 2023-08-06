from django.shortcuts import render
from requests import get


# Create your views here.

def get_symbol_icon(symbol: str) -> dict:

    url = "https://coinicons-api.vercel.app/api/icon/{symbol}"
    try:
        response = get(url=url.format(symbol=symbol))
        if response.status_code == 200:
            pass
        else:
            pass
    except Exception as error:
        raise error


def prices(request):
    return render(request, 'price_app/prices_page.html')
