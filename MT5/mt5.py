import MetaTrader5 as mt5
from MetaTrader5 import *
from datetime import datetime
import time
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#inputs:
account= 3000022295
password = 'TL0xDyKWzkM'

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    mt5.shutdown()

authorized=mt5.login(account, password=password)
if authorized:
    print("connected to account #{}".format(account))
    # print(mt5.account_info())
    # print("Show account_info()._asdict():")
    # account_info_dict = mt5.account_info()._asdict()
    # for prop in account_info_dict:
    #     print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

# get symbols
symbols=mt5.symbols_get()
count=0
for s in symbols:
    count+=1
    #print("{}. {}".format(count,s.name))
    if count==5: break


# request 1000 ticks from EURAUD
euraud_ticks = mt5.copy_ticks_from("EURAUD", datetime(2020,1,28,13), 1000, mt5.COPY_TICKS_ALL)
# request ticks from AUDUSD within 2019.04.01 13:00 - 2019.04.02 13:00
audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2020,1,27,13), datetime(2020,1,28,13), mt5.COPY_TICKS_ALL)
 
# get bars from different symbols in a number of ways
eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(2020,1,28,13), 1000)
eurgbp_rates = mt5.copy_rates_from_pos("EURGBP", mt5.TIMEFRAME_M1, 0, 1000)
eurcad_rates = mt5.copy_rates_range("EURCAD", mt5.TIMEFRAME_M1, datetime(2020,1,27,13), datetime(2020,1,28,13))
 
# shut down connection to MetaTrader 5
mt5.shutdown()
 
# #PLOT
# # create DataFrame out of the obtained data
# ticks_frame = pd.DataFrame(euraud_ticks)
# # convert time in seconds into the datetime format
# ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
# # display ticks on the chart
# plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
# plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')
# plt.legend(loc='upper left')
# plt.title('EURAUD ticks')
# plt.show()