#numerical and well known libraries:
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime as dt

#library for charts
#import mplfinance as mpf
#from mplfinance import original_flavor

#libraries for technical analysis
#import btalib
#import talib

#for metatrader integration:
#import MetaTrader5 as mt5

#importing my own libraries:
from Strategies import *
from Functions import *



btc = get_data_binance()
print(btc)