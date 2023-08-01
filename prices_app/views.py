from django.shortcuts import render

# Create your views here.

def prices(request):

    return render(request, 'price_app/prices_page.html')