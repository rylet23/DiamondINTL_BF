# This code cant run on its own via run python this file :
# To run do this: python manage.py run_trading_updates --days 2 --number 10 --seconds 30 --force


from django.core.management.base import BaseCommand
import yfinance as yf
import time
import json
from datetime import datetime, timedelta, date
import pandas_market_calendars as market_days
import sys 

from myapp.models import StockInfotable, Scroltable
from myapp.utils import TradingTime1, TradingDays

def Is_TradingHours():
    currentEastHour, currentEastMinute = TradingTime1()
    if currentEastHour < 9 or (currentEastHour == 9 and currentEastMinute < 30):
        return False
    if currentEastHour >= 16:
        return False
    return True
class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('-d', '--days', type=int, default=1)
        parser.add_argument('-n', '--number', type=int, default=5)
        parser.add_argument('-s', '--seconds', type=int, default=60)
        parser.add_argument('--force', action='store_true')

    def handle(self, *args, **options):
        days_ago = options['days']
        num_stocks = options['number']
        sec_wait = options['seconds']
        force_execution = options['force']

    
        file_path = 'myapp//management//commands//company_tickers.json'
        with open(file_path, 'r') as file:
            tickers_data = json.load(file)

        if TradingDays() and (TradingTime1() or force_execution):
            self.stdout.write(self.style.SUCCESS("Starting stock updates..."))
            self.update_stocks(tickers_data, days_ago, num_stocks)
            time.sleep(sec_wait) 
        elif force_execution:
            self.stdout.write("Forced execution outside trading hours.")
            self.update_stocks(tickers_data, days_ago, num_stocks)
        else:
            self.stdout.write(self.style.WARNING("Currently outside trading hours and no force execution requested."))

    def update_stocks(self, tickers_data, days_ago, num_stocks):
        nyse = market_days.get_calendar('NYSE')
        td = date.today()
        days = nyse.valid_days(start_date='2007-04-04', end_date=td)
        today_date = days[-1].strftime('%Y-%m-%d')
        # if len(days) < days_ago + 1:  # Ensure we have enough historical data
        #     self.stdout.write(self.style.ERROR("Not enough historical data available."))
        #     return

        yesterday_date = days[-2]
        day_compare = days[-days_ago - 1]

        max1 = float("-inf")
        min1 = float("inf")
        max_symbol = ''
        min_symbol = ''
        StockInfotable.objects.all().delete()
        count = 0
        for ticker_info in tickers_data.values():
            count+=1
            symbolz = ticker_info['ticker'].lower()
            if count <= num_stocks:
                # print("ran through all the stocks in this iteration")
                
                try:
                    countstr = str(count)
                    print(symbolz + ' ' + today_date + ' ' + countstr)
                    data1 = yf.download(tickers=symbolz, start=today_date)
                    data2 = yf.download(tickers=symbolz, start=yesterday_date)
                    data3 = yf.download(tickers=symbolz, start=day_compare)

                    pruh = data1['Close'][0]
                    pruh_yuh_close = data2['Close'][0]
                    pruh_yuh = data2['Open'][-1]
                    pruh_whenever = data3['Open'][0]


                    delta_today = ((pruh - pruh_yuh_close) / pruh_yuh_close) * 100

                    delta_yesterday = ((pruh - pruh_yuh) / pruh_yuh) * 100

                    delta_total = ((pruh - pruh_whenever) / pruh_whenever) * 100
                    

                    if delta_total > max1:
                        max1 = delta_total
                        max_symbol = symbolz

                    if delta_total < min1:
                        min1 = delta_total
                        min_symbol= symbolz

                    # Update or create StockInfo entry
                    StockInfotable.objects.update_or_create(
                        ticker=symbolz,
                        defaults={
                            'pruh': pruh,
                            'pruh_yuh_close': pruh_yuh_close, 
                            'pruh_yuh': pruh_yuh,
                            'day_compare': pruh_whenever,
                            'delta_today': delta_today,
                            'delta_yesterday': delta_yesterday,
                            'delta_total': delta_total,
                        }
                    )

                except Exception as e:
                    print(f"Error processing {symbolz}: {str(e)}")
                    continue
            else:
                break
        Scroltable.objects.all().delete()
        Scroltable.objects.create(
            max =max1, 
            min=min1, 
            max_symbol=max_symbol, 
            min_symbol=min_symbol

        )
