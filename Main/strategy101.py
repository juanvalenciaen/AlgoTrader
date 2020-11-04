#numerical and well known libraries:
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime as dt
import time

#library for charts
import mplfinance as mpf
from mplfinance import original_flavor

#libraries for technical analysis
import btalib
import talib

#for metatrader integration:
import MetaTrader5 as mt5

#importing my own libraries:
import Functions as f
import Strategies as s



symbol = 'AUDUSD' 
mins_executing= 15

trade = False
trades_list = []
trades_side = []

for min in range(1,mins_executing):
    trading_symbol = f.get_data_mt5(symbol=symbol,bars=100,timeframe='M1')
    trading_symbol = f.get_indicators(trading_symbol,fast=10)
    if trading_symbol['ma_fast'].iloc[-1] > trading_symbol['ma_slow'].iloc[-1]:
        if (trade) and side == 'short':
            for trade in trades_list:
                try:
                    f.get_closed(trade,symbol=symbol,side=side)
                print('short closed: ', trade)
            trade_list = []
        side = 'long'
        trade = f.get_order(symbol=symbol,side=side,magic=101)
        trades_list.append(trade)
        print('long executed: ',trade)
    elif trading_symbol['ma_fast'].iloc[-1] < trading_symbol['ma_slow'].iloc[-1]:
        if (trade) and side == 'long':
            for trade in trades_list:
                try:
                    f.get_closed(trade,symbol=symbol,side=side)
                print('long closed: ', trade)
            trade_list = []
        side = 'short'
        trade = f.get_order(symbol=symbol,side=side,magic=101)
        trades_list.append(trade)
        print('short executed: ',trade)
    time.sleep(65)
    print('1minute')

for trade in trades_list:
    f.get_closed(trade,symbol=symbol,side=side)
print('Time is over: ',mins_executing,' minutes')