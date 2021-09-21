import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
import requests
import datetime as dt
from dateutil.relativedelta import relativedelta
import dateutil.parser
import pytz
import math
#following are the ones can cause problems:
import websocket, json
import mplfinance as mpf
from mplfinance import original_flavor
import MetaTrader5 as mt5
import backtrader as bt
#import talib

#importing from my own library
import config


#getting data
def get_data(symbol='BTC-USD', months=12,source='yahoo'):
  n_days = dt.timedelta(days=(int(months*30)))
  end = dt.date.today()
  start = end - n_days
  df = web.DataReader(symbol, source, start, end)
  df['symbol'] = symbol
  df = df[['symbol', 'Open', 'High', 'Low', 'Close','Adj Close', 'Volume']]
  return df

def get_data_yh(symbol='BTC-USD',years=1):
    # Get today's date as UTC timestamp
    today = dt.datetime.today().strftime("%d/%m/%Y")
    today = dt.datetime.strptime(today + " +0000", "%d/%m/%Y %z")
    to = int(today.timestamp())
    # Get date ten years ago as UTC timestamp
    ten_yr_ago = today-relativedelta(years=years)
    fro = int(ten_yr_ago.timestamp())
    # Put stock price data in dataframe
    url = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={fro}&period2={to}&interval=1d&events=history".format(symbol=symbol, fro=fro, to=to)
    data = pd.read_csv(url)
    # Convert date to timestamp and make index
    data.index = data["Date"].apply(lambda x: pd.Timestamp(x))
    data.drop("Date", axis=1, inplace=True)
    data['symbol'] = symbol
    data = data[['symbol', 'Open', 'High', 'Low', 'Close','Adj Close', 'Volume']]
    return data

def get_data_yh_intraday(symbol='BTC-USD',timeframe='60m',days=30):
    n_days = dt.timedelta(days=days)
    end = dt.date.today()
    start = end - n_days
    df = yf.download(symbol, start, end, interval=timeframe)
    df['symbol'] = symbol
    df = df[['symbol', 'Open', 'High', 'Low', 'Close','Adj Close', 'Volume']]
    return df



def get_data_mt5(symbol='EURUSD',bars=500,to=0, timeframe='H1'):
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    concatenation = 'mt5.TIMEFRAME_' + timeframe
    evaluated = eval(concatenation)
    rates = mt5.copy_rates_from_pos(symbol, evaluated, 0, bars)
    mt5.shutdown()
    df = pd.DataFrame(rates)
    df.time = pd.to_datetime(df.time, unit='s')
    df = df.set_index('time')
    df['symbol'] = symbol
    df = df.rename(columns={'open': 'Open','high':'High','low':'Low','close':'Close','tick_volume':'Volume'})
    df = df[['symbol', 'Open', 'High', 'Low', 'Close', 'Volume','spread','real_volume']]
    return(df)

#get inputs (symbol, and source) from here https://www.tensorcharts.com/tensor/markets
def get_data_tensor(timeframe='1h',mode=2,extra_data=True,symbol='XBTUSD',source='bitmex'):
    if mode == 1:
        url = 'https://www.tensorcharts.com/tensor/bitmex/{}/bitmexStats/{}/0'.format(symbol,timeframe)
        data = requests.get(url).json()
        times = pd.to_datetime([e['timestamp'] for e in data])
        candles = [(e['price']) for e in data]
        df = pd.DataFrame(index=times, data=candles)
        df = df.rename(columns={0:'Open',1:'High',2:'Low',3:'Close'})
        df['symbol'] = symbol
        df = df[['symbol','Open', 'High', 'Low', 'Close']]
        if extra_data:
            stats = [(e['buyLiquidations'],e['sellLiquidations'],e['openInterest'],e['openValue'],e['fundingRate'],e['fundingRateDaily'],e['indicativeFundingRate'],e['turnover'],e['turnover24h'],e['totalTurnover']) for e in data]
            df_stats = pd.DataFrame(index=times, data=stats)
            df_stats = df_stats.rename(columns={0:'buyLiquidations',1:'sellLiquidations',2:'openInterest',3:'openValue',4:'fundingRate', 5:'fundingRateDaily', 6:'indicativeFundingRate', 7:'turnover',8:'turnover24h',9:'totalTurnover'})
            df = df.join(df_stats)
    elif mode == 2:
        url = 'https://www.tensorcharts.com/tensor/{}/{}/heatmapCandles/{}'.format(source,symbol,timeframe)
        data = requests.get(url).json()
        times = pd.to_datetime([e['T'] for e in data])
        candles = [(e['open'],e['close'],e['high'],e['low'],e['volume']) for e in data]
        df = pd.DataFrame(index=times, data=candles)
        df = df.rename(columns={0:'Open',1:'Close',2:'High',3:'Low',4:'Volume'})
        df['symbol'] = symbol
        df = df[['symbol','Open', 'High', 'Low', 'Close','Volume']]
        if extra_data:
            stats = [(e['buyVolume'],e['sellVolume'],e['askVolume'],e['bidVolume'],e['vwap'],e['maxOrderBookHeatmapPointVolume'],e['maxOrderBook2HeatmapPointVolume'],e["heatmapStepVolume"],e["heatmapStep"]) for e in data]
            df_stats = pd.DataFrame(index=times, data=stats)
            df_stats = df_stats.rename(columns={0:'buyVolume', 1:'sellVolume', 2:'askVolume', 3:'bidVolume', 4:'vwap', 5:'maxOrderBookHeatmapPointVolume', 6:'maxOrderBook2HeatmapPointVolume',7:"heatmapStepVolume",8:"heatmapStep"})
            df = df.join(df_stats)
            orderbooks = [(e['heatmapOrderBook'] or []) for e in data]
            prices = sorted(set(prc for ob in orderbooks for prc in ob[::2]))
            vol_matrix = [[0]*len(prices) for _ in range(len(times))]
            for i,orderbook in enumerate(orderbooks):
                for price,volume in zip(orderbook[::2],orderbook[1::2]):
                    j = prices.index(price)
                    vol_matrix[i][j] = volume
            df_heatmap = pd.DataFrame(index=times, columns=prices, data=vol_matrix)
            df_heatmap = df_heatmap.add_prefix('OB: ')
            # plt.bar(x=df_heatmap.T.index, height=df_heatmap.iloc[0])
            # plt.show()
            df = df.join(df_heatmap)
    return df

def get_data_binance(symbol='BTCUSDT', start_time='2020-06-22', end_time='2020-06-25',interval_mins=60):
    utc2timestamp = lambda s: int(dateutil.parser.parse(s).replace(tzinfo=pytz.utc).timestamp() * 1000)
    interval_ms = 1000*60*interval_mins
    interval_str = '%sm'%interval_mins if interval_mins<60 else '%sh'%(interval_mins//60)
    start_time = utc2timestamp(start_time)
    end_time = utc2timestamp(end_time)
    data = []
    for start_t in range(start_time, end_time, 1000*interval_ms):
        end_t = start_t + 1000*interval_ms
        if end_t >= end_time:
            end_t = end_time - interval_ms
        url = 'https://www.binance.com/fapi/v1/klines?interval=%s&limit=%s&symbol=%s&startTime=%s&endTime=%s' % (interval_str, 1000, symbol, start_t, end_t)
        print(url)
        d = requests.get(url).json()
        data += d
    df = pd.DataFrame(data, columns='time open high low close volume a b c d e f'.split())
    df = df.astype({'time':'datetime64[ms]', 'open':float, 'high':float, 'low':float, 'close':float, 'volume':float})
    df = df.rename(columns={'open':'Open',"close": "Close", "high": "High",'low':'Low','volume':'Volume'})
    df['symbol'] = symbol
    df = df.set_index('time')
    return df



#charting
def chart(df, type='candle',vol=False,MA=False,log=False):
  name = df['symbol'].iloc[0]
  if log:
    df.Close = np.log(df.Close)
    df.Open = np.log(df.Open)
    df.High = np.log(df.High)
    df.Low = np.log(df.Low)
  if MA:
    mpf.plot(df,type=type,style='charles',volume=vol,mav=MA,figratio=(20,10), title='Chart: '+ name,ylabel='price')
  else:
    mpf.plot(df,type=type,style='charles',volume=vol,figratio=(20,10), title='Chart: '+ name,ylabel='price')

def chart_(df,log=False,vol=False):
  fig = plt.figure(figsize=(15,10))
  ax1 = fig.add_axes([0.05, 0.21, 0.93, 0.75])
  plt.grid(True)
  fig.autofmt_xdate()
  name = df['symbol'].iloc[0]
  plt.title('Chart: ' + name)
  if log:
    df.Close = np.log(df.Close)
    df.Open = np.log(df.Open)
    df.High = np.log(df.High)
    df.Low = np.log(df.Low)
  original_flavor.candlestick2_ochl(ax1,df.Open, df.Close, df.High, df.Low, width=0.6, colorup='green', colordown='r')
  if vol:
    ax2 = fig.add_axes([0.05, 0.03, 0.93, 0.20],sharex=ax1) 
    original_flavor.volume_overlay(ax2, df.Open, df.Close, df.Volume, colorup='green', colordown='r',width=0.8, alpha=0.5)
  plt.show()



#ajustar el precio a los datos de cierre ajustados (para splits, dividendos, etc)
def adjusted(df):
    df=df.copy()
    lista=['Open','High','Low']
    for f in lista:
        df[f]=df[f]*df['Adj Close']/df['Close']
    df=df.drop('Close', axis=1)
    df=df.rename(columns = {'Adj Close': 'Close'} )
    return df


#run this code in another IDE because talib library doesnt run here
# to install talib: https://blog.quantinsti.com/install-ta-lib-python/
import talib

#get indicators
def get_indicators(data,fast=20,slow=50):
    # Get MACD
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])
    # Get RSI
    data["rsi"] = talib.RSI(data["Close"])
    # Get MAS and crossover
    data["ma_fast"] = talib.MA(data["Close"], timeperiod=fast)
    data["ma_slow"] = talib.MA(data["Close"], timeperiod=slow)
    data['prev_ma_fast'] = data['ma_fast'].shift(1)
    # data['prev_ma_slow'] = data['ma_slow'].shift(1)
    # data['ma_cross'] = np.where(data['ma_fast'] > data['ma_slow'] and data['prev_ma_fast'] < data['prev_ma_slow'],1,0)
    #get candle patterns
    data['engulfing'] = talib.CDLENGULFING(data.Open, data.High, data.Low, data.Close)
    data['morningstar'] = talib.CDLMORNINGSTAR(data.Open, data.High, data.Low, data.Close)
    return data


def EMA(df, n):
  EMA = pd.Series(pd.Series.ewm(df['Close'], span = n, min_periods = n-1, adjust = False).mean(), name = 'EMA_' + str(n))
  df = df.join(EMA)
  return df

# #get signal:

# #encode as 0, 1, and -1 for no signal, long and short
# #couldn't make a function to simplify it so...
# #you must copy and paste the following code:

# data['signal'] = np.where(data[indicador1] > data[indicador2], 1,np.nan)
# data['signal'] = np.where(data[indicador1] < data[indicador2], -1,data['signal'])


# #turn a signal into a position

#converts a signal 1, or -1
#into a position maintaining the state -1 and +1 until it changes
def signal_to_position(df,signal,side=False):
    df['position'] = df[signal]
    i=0
    for row in df.T:
        if df['position'].iloc[i] == 0 and i>0:
            if df['position'].iloc[i-1] != 0:
                df['position'].iloc[i] = df['position'].iloc[i-1]
        i+=1
    df['position'] = np.where(df['position'] > 0, 1,df['position'])
    df['position'] = np.where(df['position'] < 0, -1,df['position'])
    if side == 'long':
      df['position'] = np.where(df['position'] < 0, 0,df['position'])
    elif side == 'short':
      df['position'] = np.where(df['position'] > 0, 0,df['position'])
    return df





#plot trades in a chart:
#to plot any signal
#must be encoded as 0, 1, and -1
def plot_signal(df, signal, position=False,lines=False):
  name = (df.reset_index())['symbol'].iloc[0]
  buys = df[df[signal] > 0].index
  sells = df[df[signal] < 0].index
  fechas = []
  colores = []
  Trades = []
  for trade in buys:
    fechas.append(trade)
    colores.append('g')
  for trade in sells:
    fechas.append(trade)
    colores.append('r')
  df_trades = pd.DataFrame({'colors':colores}, index= fechas)
  df = df.join(df_trades)
  df['buy_price'] = np.where(df['colors'] == 'g', df['Close'], math.nan)
  df['sell_price'] = np.where(df['colors'] == 'r', df['Close'], math.nan)
  if position:
    lines = True
  if lines:
    marker = 0.1
    if position:
      width = 0.3
      alpha = 0.1
    else:
      width = 0.5
      alpha = 0.7
  else:
    width = 0.01
    alpha = 0.01
    marker = 70
  if df['buy_price'].notnull().sum().sum() > 0:
    trades_buy = mpf.make_addplot(df['buy_price'],type='scatter',markersize=marker,marker='^',color='g')
    Trades.append(trades_buy)
  if df['sell_price'].notnull().sum().sum() > 0:
    trades_sell = mpf.make_addplot(df['sell_price'],type='scatter',markersize=marker,marker='v',color='r')
    Trades.append(trades_sell)
  mpf.plot(df,type='candle',style='charles',figratio=(16,8), addplot=Trades, vlines=dict(vlines=fechas,colors=colores,linewidths=width,alpha=alpha), title=name + ' daily chart'+ ' signal:' + signal,ylabel='price')




def plot_signal_(df, signal):
  fig = plt.figure(figsize=(12,6))
  ax1 = plt.subplot()
  original_flavor.candlestick2_ochl(ax1,df.Open, df.Close, df.High, df.Low, width=0.5, colorup='green', colordown='r')
  plt.grid(True)
  fig.autofmt_xdate()
  df = df.reset_index()
  name = df['symbol'].iloc[0]
  plt.title('Chart ' + name + ' signal: ' + signal)
  trigger_buys = df[df[signal] > 0]['Date']
  trigger_sells = df[df[signal] < 0]['Date']
  buys = trigger_buys.index
  sells = trigger_sells.index
  for trade in buys:
    ax1.axvline(x=trade, color='g',alpha=0.6)
  for trade in sells:
    ax1.axvline(x=trade, color='r',alpha=0.6)
  plt.show()

def plot_morningstar(symbol, n_months=12):
  if isinstance(symbol, str):
    df = get_data(symbol, n_months)
  else:
    df = symbol
  df['morningstar'] = talib.CDLMORNINGSTAR(df.Open, df.High, df.Low, df.Close)
  chart_signal(df, 'morningstar')





#backtest a strategy


def plot_backtest(data, position=False,returns='simple',leverage=1):
  if ('strategy' in data) == False:
    #data[position] = data[position].fillna(0)
    if returns == 'simple':
      data['returns'] = (data['Close'] /data['Close'].shift(1))
    elif returns== 'log':
      data['returns'] = np.log(data['Close'] /data['Close'].shift(1))+1
    data['position'] = data['position'] * leverage
    data['strategy'] = (data['returns'] ** data[position].shift(1))
    data = data[['Close',position, 'returns', 'strategy']]
  print(' Strategy Return = ', round(data['strategy'].dropna().cumprod()[-1] *100,2), '%')
  print(' VS Market Return = ', round(data['returns'].dropna().cumprod()[-1] *100,2), '%')
  plt.style.use('seaborn')
  data[['returns', 'strategy']].dropna().cumprod().plot(figsize=(14,6))
  plt.show()


#backtest using backtrader:

def backtrader(data, strategy,init=100000.0):
  #name = data['symbol'].iloc[0]
  cerebro = bt.Cerebro()
  cerebro.broker.setcash(init)
  feed = bt.feeds.PandasData(dataname=data)
  cerebro.adddata(feed)
  cerebro.addstrategy(strategy)
  print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
  cerebro.run()
  print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
  final = cerebro.broker.getvalue()
  Return = ((final/init)-1)* 100
  print('Return: ', int(Return), '%')
  cerebro.plot()




#To Connect alpaca api data

def conect_data(symbols=['FB','AMZN','AAPL','NFLX','GOOGL'], type='t'):
  def on_open(ws):
      print("opened")
      auth_data = {
          "action": "authenticate",
          "data": {"key_id": config.API_KEY,"secret_key": config.SECRET_KEY}}
      ws.send(json.dumps(auth_data))
      concatenation = []
      i=0
      for sym in symbols:
        if type == 't':
          concatenation.append('T.'+symbols[i])
          i+=1
        elif type == 'm':
          concatenation.append('MA.'+symbols[i])
          i+=1
      print(concatenation)
      if type == 't':
        print('Tick data')
      elif type == 'm':
        print('Minute data')
      listen_message = {"action":"listen","data":{"streams":concatenation}}
      ws.send(json.dumps(listen_message))
  def on_message(ws, message):
      print("received a message")
      print(message)
  socket = "wss://data.alpaca.markets/stream"
  ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)#, on_close=on_close)
  ws.run_forever()






#Send order to MT5

def get_order(symbol='EURUSD', side='long', lot=0.01,sl=100,tp=100,magic=101):
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    # prepare the buy request structure
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()
    point = mt5.symbol_info(symbol).point
    ask = mt5.symbol_info_tick(symbol).ask
    bid = mt5.symbol_info_tick(symbol).bid
    if side == 'long':
        price = ask
        stop_loss = price - sl * point
        take_profit = price + tp * point
        type_side = mt5.ORDER_TYPE_BUY
    elif side == 'short':
        price = bid
        stop_loss = price + sl * point
        take_profit = price - tp * point
        type_side = mt5.ORDER_TYPE_SELL
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": type_side,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": deviation,
        "magic": magic,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        #"type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    #print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        #for field in result_dict.keys():
            #print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            # if field=="request":
            #     traderequest_dict=result_dict[field]._asdict()
                # for tradereq_filed in traderequest_dict:
                #     print("  traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        #print("shutdown() and quit")
        mt5.shutdown()
        #quit()
    #print("2. order_send done, ", result)
    #print("   opened position with POSITION_TICKET={}".format(result.order))
    return result.order



def get_closed(trade, symbol='EURUSD',side='long',lot=0.01,magic=102):
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    # prepare the buy request structure
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()
    # create a close request
    ask = mt5.symbol_info_tick(symbol).ask
    bid = mt5.symbol_info_tick(symbol).bid
    if side == 'short':
          price = ask
          type_side = mt5.ORDER_TYPE_BUY
    elif side == 'long':
          price = bid
          type_side = mt5.ORDER_TYPE_SELL
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": type_side,
        "position": trade,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        #"type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result=mt5.order_send(request)
    # check the execution result
    #print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(trade,symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        #print("   result",result)
    else:
        #print("4. position #{} closed, {}".format(trade,result))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        # for field in result_dict.keys():
        #     #print("   {}={}".format(field,result_dict[field]))
        #     # if this is a trading request structure, display it element by element as well
        #     if field=="request":
        #         traderequest_dict=result_dict[field]._asdict()
        #         for tradereq_filed in traderequest_dict:
        #             #print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()