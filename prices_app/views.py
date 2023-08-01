from django.shortcuts import render

from typing import Tuple
# Create your views here.

def get_price(symbol: str) -> Tuple[str, int]:
    pass



def prices(request):

    return render(request, 'price_app/prices_page.html')