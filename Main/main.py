#run this talib library you'll need to use yout own IDE
# to install talib: https://blog.quantinsti.com/install-ta-lib-python/
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas_datareader.data as web
import datetime as dt
import mplfinance as mpf
from mplfinance import original_flavor
import btalib
import talib
import MetaTrader5 as mt5
#importing my own libraries
import Functions as f
import Strategies as s

# df = f.get_data()

# f.chart(df,vol=True,)

# #f.plot_morningstar('AMD',60)

# #f.conect_data(['SPY','AAPL','TUP','CL'],'t')


# # rsi = btalib.rsi(df)
# # df['rsi'] = rsi.df
# # df['rsi_signal'] = np.where(df['rsi'] > 75,-1,0)
# # df['rsi_signal'] = np.where(df['rsi'] < 25,1,df['rsi_signal'])
# # #f.plot_signal(df, 'rsi_signal')

# # df = f.get_data('AMD',months=10,source='yahoo')
# # ind = f.get_indicators(df)
# # f.chart(ind,log=True,vol=True,MA=(20,50,100))
# # f.plot_signal(ind,'morningstar',lines=True,marker=1)
# # ind['position'] = np.where(ind['ma_fast'] > ind['ma_slow'], 1,0)
# # ind['position'] = np.where(ind['ma_fast'] < ind['ma_slow'], -1,ind['position'])



# data = f.get_data_()
# data['price'] = data['Adj Close']
# SMA = 25
# data['SMA'] = data['price'].rolling(window=SMA).mean()
# N = 1
# data['STD'] = N*data['price'].rolling(window=SMA).std()
# data['SMA+STD'] = data['SMA'] + data['STD']
# data['SMA-STD'] = data['SMA'] - data['STD']
# plt.style.use('seaborn')
# #data[['price','SMA+STD','SMA-STD']].plot(figsize=(24,6))
# data['position'] = np.where(data['price'] > data['SMA+STD'], -1,0)
# data['position'] = np.where(data['price'] < data['SMA-STD'], 1,data['position'])

# f.plot_signal(data,'position',lines=True,marker=1)



# # ko_m5 = f.get_data_mt5('KO',bars=200,timeframe='M5')
# # print(ko_m5)
# # f.chart_(ko_m5,vol=True)
# # f.backtrader(ko_m5,strategy=s.TestStrategy)
# # f.get_order(symbol='KO',lot=1.0)


# # symbols=['TSLA', 'AAPL', 'AMZN', 'NFLX']
# # f.conect_data()




df = f.get_data_yh(years=2,symbol='TSLA')
df = f.get_indicators(df)
# #print(df)
df = f.signal_to_position(df,'engulfing',side='long')

# #f.plot_signal(df,'morningstar',lines=True)
f.plot_backtest(df, 'position',returns='simple',leverage=1)
# # position = f.backtest(df,'position')
# # f.plot_backtest(position)




# # data =f.get_data_tensor(timeframe='4h',mode=2,symbol='ETHUSD',extra_data=True)
# data = f.get_data_binance(symbol='BTCUSDT',start_time='2020-06-22', end_time='2020-06-25',interval_mins=60)
# print(data)
# f.chart(data,vol=True)
