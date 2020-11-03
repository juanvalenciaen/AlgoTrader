import os, sys, argparse
import pandas as pd
import pandas_datareader.data as pdr
import datetime as dt
import backtrader as bt

#importing my strategies from other files
from strategies import TestStrategy
from GoldenCross import GoldenCross
from BuyHold import BuyHold

#this is for selecting the strategy
"""
strategies = {
    "golden_cross": GoldenCross,
    "buy_hold": BuyHold,
    "test": TestStrategy
}
parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="which strategy to run", type=str)
args = parser.parse_args()

if not args.strategy in strategies:
    print("invalid strategie, must be one of {}".format(strategies.keys()))
    sys.exit()
"""
#data inputs
symbol = 'SPY'
n_months = 84
#data download
n_days = dt.timedelta(days=(int(n_months*30)))
end = dt.date.today()
start = end - n_days
df = pdr.DataReader(symbol, 'yahoo', start, end)

cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000)
feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)
#next you can input the strategy you want to test
cerebro.addstrategy(GoldenCross)
#cerebro.addstrategy(strategies[args.strategy])
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()