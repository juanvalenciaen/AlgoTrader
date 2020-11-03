import btalib
import pandas as pd
import pandas_datareader.data as pdr
import datetime as dt

df = pdr.DataReader('BTC-USD','yahoo', start=(dt.datetime(2020,1,1)),end=(dt.datetime(2020,10,1)))
#df = pd.read_csv('data/ohlc/AAPL.csv', parse_dates=True, index_col='Date')

sma = btalib.sma(df, period=50)
df['sma'] =sma.df

rsi = btalib.rsi(df)
df['rsi'] =rsi.df

print(df)