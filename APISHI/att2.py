import sqlite3
import yfinance as yf
import time
import json as js
from TradingTime import TradingTime1, TradingDays
from datetime import date, timedelta
import pandas_market_calendars as MarketDays
# added for postgre DB
import psycopg2
import psycopg2.extras
import os
from passwords import passpee
key1,dbname1,user1,password1,host1 = passpee()


def Is_TradingHours():
    currentEastHour, currentEastMinute = TradingTime1()
    if currentEastHour < 9 or (currentEastHour == 9 and currentEastMinute < 30):
        return False
    if currentEastHour >= 16:
        return False
    return True

nyse = MarketDays.get_calendar('NYSE')
td = date.today()
days = nyse.valid_days(start_date='2007-04-04', end_date=td)
today_date = days[-1]
today_date.strftime('%Y-%m-%d')
yesterday_date = today_date - timedelta(days=1)
while True:
    day_input = input("How many days ago do you want to compare the data to? ")
    try:
        days_ago = int(day_input)
        if days_ago > 0:
            break
        else:
            print('not a positive whole number, re-enter number of days')
    except ValueError:
        print("Not a valid number, re-enter number of days")

while True:
    Numb_ask = input("How many stocks do you want to execute? ")
    try:
        Numb_Stocks = int(Numb_ask)
        if Numb_Stocks > 0:
            break
        else:
            print('not a positive whole number, re-enter number of stocks')
    except ValueError:
        print("Not a valid number, re-enter number of stocks")

while True:
    sec_ask = input("How many seconds would you like to wait between each execution? ")
    try:
        sec_wait = int(sec_ask)
        if sec_wait > 0:
            break
        else:
            print("Not a positive number, re-enter number of seconds")
    except ValueError:
        print("Not a valid number, re-enter number of seconds")

day_compare = today_date - timedelta(days=days_ago)
#Include APISHI//company_tickers.json when running within full system
file_path = 'company_tickers.json'
with open(file_path, 'r') as JSONfile:
    tickers_data = js.load(JSONfile)
    con = psycopg2.connect(dbname=dbname1, user=user1, password=password1, host=host1)
curr = con.cursor()
curr.execute('CREATE TABLE IF NOT EXISTS StockInfo1 (Ticker TEXT PRIMARY KEY, Price REAL, Open_Price REAL, Yesterday_Price REAL, Day_Ago_Price REAL, Delta_Today REAL, Delta_Yesterday REAL, Delta_Total REAL)')
con.commit()
def stocktable():
    count = 0

    for ticker_info in tickers_data.values():
        count+=1
        if count <= Numb_Stocks:
            symbolz = ticker_info['ticker'].lower()
            try:
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
                
                curr.execute('''INSERT INTO StockInfo1 (Ticker, Price, Open_Price, Yesterday_Price, Day_Ago_Price, Delta_Today, Delta_Yesterday, Delta_Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (Ticker) DO UPDATE SET Price = EXCLUDED.Price, Open_Price = EXCLUDED.Open_Price, Yesterday_Price = EXCLUDED.Yesterday_Price, Day_Ago_Price = EXCLUDED.Day_Ago_Price, Delta_Today = EXCLUDED.Delta_Today, Delta_Yesterday = EXCLUDED.Delta_Yesterday, Delta_Total = EXCLUDED.Delta_Total''', (symbolz, pruh, pruh_yuh_close, pruh_yuh, pruh_whenever, delta_today, delta_yesterday, delta_total))
                # print(pruh +":" + symbolz)
                con.commit()

                
            except Exception as e:
                print(f"Error processing {symbolz}: {str(e)}")
                continue


while Is_TradingHours() and TradingDays():
    stocktable()
    print("Going thru again in " + str(sec_wait) + " seconds.")
    time.sleep(sec_wait)
else:
    still_work = input("Outside trading hours, do you still want to execute?(yes or no)? ")
    if still_work == 'yes':
        curr.execute('DROP TABLE IF EXISTS StockInfo1')
        curr.execute('CREATE TABLE StockInfo1 (Ticker TEXT PRIMARY KEY, Price REAL, Open_Price REAL, Yesterday_Price REAL, Day_Ago_Price REAL, Delta_Today REAL, Delta_Yesterday REAL, Delta_Total REAL)')
        stocktable()
        print("After hours information displayed.")
    else:
        print("Okay")
