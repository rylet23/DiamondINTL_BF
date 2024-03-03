from django.urls import path
from . import views

# app_name = 'myapp'

urlpatterns = [
    # Translated from Flask's app.route decorators
    path('', views.sign_in, name = 'sign_in'),
    # path('signin/', views.sign_in, name='sign_in'),  # Assuming the root route ('/') and '/Signin' both use the sign_in view
    path('account/', views.account, name='account'),
    path('account/portfolio/', views.portfolio, name='portfolio'),
    path('account/settings/', views.settings_view, name='settings_view'),
    path('metals/', views.Metals, name='metals'),
    path('metals/gold/', views.goldDirect, name='gold_direct'),
    path('metals/silver/', views.silverDirect, name='silver_direct'),
    path('crypto/', views.Crypto, name='crypto'),
    path('bonds/', views.Bonds, name='bonds'),
    path('trades/', views.trades, name='trades'),
    # path('scrolly/', views.scrolly, name='scrolly'),
    path('trades/etfs/', views.etfDirect, name='etf_direct'),
    path('trades/options/', views.optionsDirect, name='options_direct'),
    path('trades/mutualfunds/', views.mfDirect, name='mf_direct'),
    path('trades/reits/', views.reitDirect, name='reit_direct'),
    # Add more paths as needed...
]