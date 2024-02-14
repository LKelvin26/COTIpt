from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def convertidor_tasas(request):
    return render(request, 'tasadeCambio.html')

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def usdtomxn(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            return JsonResponse({'success': False, 'error': 'No amount provided'}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid amount'}, status=400)
        
        
        try:
            exchange_rate1 = get_exchange_rate_from_exchangerate_api()
            exchange_rate2 = get_exchange_rate_from_open_exchange_rates()
            if exchange_rate1 is None:
                    raise Exception("Both API requests failed")
            mxn_amount1 = amount * exchange_rate1
            mxn_amount2= amount * exchange_rate2 
           
            return JsonResponse({'success': True, 'valorMXNER': mxn_amount1,'valorMXNOE': mxn_amount2})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

def get_exchange_rate_from_exchangerate_api():
    url = 'https://v6.exchangerate-api.com/v6/c80245d54378a3f9fb47a23a/latest/USD'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['conversion_rates']['MXN']
    else:
        return None

def get_exchange_rate_from_open_exchange_rates():
    url = 'https://openexchangerates.org/api/latest.json?app_id=3b58bbae7f0f456cb3160042f6fddfa7&symbols=MXN'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['rates']['MXN']
    else:
        return None