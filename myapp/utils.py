# import pandas_market_calendars as mcal
# import pytz
# from datetime import datetime
# import pandas as pd
# def trading_time():
#     eastern = pytz.timezone('US/Eastern')
#     now = datetime.now(eastern)
#     return now.hour, now.minute

# def is_trading_day():
#     nyse = mcal.get_calendar('NYSE')
#     today_utc = pd.Timestamp.now(tz='UTC').floor('1D')
#     return today_utc in nyse.valid_days(start_date='2007-04-04', end_date=today_utc)

# # Dont think I need this as its repeated in utils.py

import pandas_market_calendars as MarketDays
from datetime import date, timedelta, datetime
import pytz
import pandas as pd
def TradingTime1():
    currentEastTime = pytz.timezone('US/Eastern')
    currentTime = datetime.now(currentEastTime)
    return currentTime.hour, currentTime.minute
# TradingTime1()

nyse = MarketDays.get_calendar('NYSE')
td = date.today()
days = nyse.valid_days(start_date='2007-04-04', end_date=td)
# print(days[-1])
# tdy = td - timedelta(days=2)
def TradingDays():
    td1 = pd.to_datetime(td).tz_localize('UTC')
    for day in days:
        if day == td1:
            return True
    return False
# if TradingDays() is False:
#     currentDay == 
# TradingDays()