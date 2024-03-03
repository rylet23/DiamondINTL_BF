from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import os
from .models import StockInfotable, Scroltable
from django.db import connection
# Example of loading ACCESS_KEY from .env (make sure you've loaded .env in settings.py)
ACCESS_KEY = os.getenv('ACCESS_KEY')

def user_is_authenticated(request):
    return request.session.get('authenticated', False)

def sign_in(request):
    if request.method == "POST":
        key = request.POST.get('secret_key')
        if key == ACCESS_KEY: 
            request.session['authenticated'] = True
            return redirect('account')
        else:
            return render(request, 'signin.html')
    return render(request,'signin.html')

def account(request):
    if user_is_authenticated(request):
        return render(request, 'account.html')
    return redirect('sign_in')

def portfolio(request):
    if user_is_authenticated(request):
        return render(request, 'portfolio.html')
    return redirect('sign_in')

def settings_view(request):
    if user_is_authenticated(request):
        return render(request, 'settings.html')
    return redirect('sign_in')

def Metals(request):
    if user_is_authenticated(request):
        return render(request, 'metals.html')
    return redirect('sign_in')

def goldDirect(request):
    if user_is_authenticated(request):
        return render(request, 'gold.html')
    return redirect('sign_in')

def silverDirect(request):
    if user_is_authenticated(request):
        return render(request, 'silver.html')
    return redirect('sign_in')

def Crypto(request):
    if user_is_authenticated(request):
        return render(request, 'crypto.html')
    return redirect('sign_in')

def Bonds(request):
    if user_is_authenticated(request):
        return render(request, 'bonds.html')
    return redirect('sign_in')

def trades(request):
    if user_is_authenticated(request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM myapp_stockinfotable")
            rows = dictfetchall(cursor)
        return render(request, 'trades.html', {'rows': rows})
        # cursor.execute("SELECT * FROM ScrolTable")
        
    return redirect('sign_in')

    # return render(request, 'trades.html', {'rows': rows})
        

# def scrolly(request):
#     if not is_authenticated(request):
#         return redirect('sign_in')
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM Scroltable")
#         rows = dictfetchall(cursor)

#     return render(request, 'trades.html', {'cols': rows})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def etfDirect(request):
    if user_is_authenticated(request):
        return render(request, 'etfs.html')
    return redirect('sign_in')

def optionsDirect(request):
    if user_is_authenticated(request):
        return render(request, 'options.html')
    return redirect('sign_in')

def mfDirect(request):
    if user_is_authenticated(request):
        return render(request, 'mutualfunds.html')
    return redirect('sign_in')

def reitDirect(request):
    if user_is_authenticated(request):
        return render(request, 'reits.html')
    return redirect('sign_in')
