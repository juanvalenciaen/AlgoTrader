import backtrader as bt
import datetime as dt
import pandas as pd
import pandas_datareader.data as pdr

#importing my own library
from strategies import TestStrategy

#backtrader data setup s
cerebro = bt.Cerebro()
cerebro.broker.set_cash(1000000)
data = bt.feeds.YahooFinanceCSVData(
    dataname = 'TUP.csv',
    fromdate=dt.datetime(2019,12,1),
    todate=dt.datetime(2020,8,1),
    reverse=False
)
cerebro.adddata(data)

#
cerebro.addstrategy(TestStrategy)
cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

#running backtrader cerebro
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()