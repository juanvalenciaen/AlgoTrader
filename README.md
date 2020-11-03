# AlgoTrader
Algorithmic Trading resources, for personal, and team usage.

Repetitive trading processes are packed through very simplified and standarized functions

## folder from_courses:
it has a compilation of script from courses, videos, blogs, online, etc.

for educatinal purposes only

## go to folder: Main

### Introduction.ipynb

is the jupyter notebook to introduce you through the functions


### Functions.py
 this is the file where functions are stored
 
 
 **Functions designed for:**
 
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
   
 ### Strategies.py
 this is the place where strategies (datatype class)
 are placed. 
 
 These are strategies to backtest or apply with frameworks such as Backtrader, Lean, and Zipline
