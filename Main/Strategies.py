import pandas as pd
import datetime as dt
import math
import numpy as np
import backtrader as bt

class BuyHold(bt.Strategy):

    def next(self):
        size = int(self.broker.getcash() / self.data)
        self.buy(size=size)

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))
            self.bar_executed = len(self)
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                #close lower than previous close
                if self.dataclose[-1] < self.dataclose[-2]:
                    #previous close lower than 2 bars previous

                    #set a BUY
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATE {}'.format(self.dataclose[0]))
                self.order = self.sell()

class GoldenCross(bt.Strategy):
    params = (('fast', 50), ('slow',200), ('order_percentage', 0.95), ('ticker', 'X'))
    
    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period =self.params.fast, plotname='50 day MA'
        )
        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period = self.params.slow, plotname='200 day MA'
        )
        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("Buy {} shares of {} at {} ".format(self.size, self.params.ticker, self.data.close[0]))

                self.buy(size=self.size)

        if self.position.size >0:
            if self.crossover < 0:
                print('Sell {} shares of {} at {} '.format(self.size, self.params.ticker, self.data.close[0]))
                self.close()

class RSI(bt.Strategy):
    params = (('order_percentage', 0.95), ('ticker', 'X'))
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(
            self.data.close, plotname='RSI'
        )
        self.oversold = self.rsi < 25
        self.overbought = self.rsi > 75
        #print(self.rsi[0])
    def next(self):
        if self.position.size == 0:
            if self.oversold:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("Buy {} shares of {} at {} ".format(self.size, self.params.ticker, self.data.close[0]))

                self.buy(size=self.size)

        if self.position.size >0:
            if self.overbought==True:
                print('Sell {} shares of {} at {} '.format(self.size, self.params.ticker, self.data.close[0]))
                self.close()