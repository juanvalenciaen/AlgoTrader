# AlgoTrader
Algorithmic Trading resources, for personal, and team usage.


##Folder: Main

###Functions 
 this is the file where functions are stored
 
 functions designed for:
 
 - get financial data from different sources (keeping the format: symbol, Open, High, Low, Close, Volume)
 
 - chart/plot the financial data
 
 - add technical indicators to DataFrames
 
 - convert indicators into signal:
   1: Long entry
  -1: Short entry
   0: No signal
   
  - convert signals into position:
    1: long position
    -1: short position
    0: out of market
    
   - plot a signal or a position in a chart
   
   - backtest a position
   
   
   There are also some functions using Backtrader, and other backtesting frameworks
   
   theres another function to make an entry in MetaTrader 5
