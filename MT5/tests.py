import datetime as dt
import MetaTrader5 as mt5
import pandas as pd

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

# df = get_data_mt5('EURUSD')
# print(df)









import time
 

def get_order(symbol='USDJPY', side='buy', lot=0.01,sl=100,tp=100):
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
    if side == 'buy':
        price = ask
        stop_loss = price - sl * point
        take_profit = price + tp * point
        type_side = mt5.ORDER_TYPE_BUY
    elif side == 'sell':
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
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        #"type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                # for tradereq_filed in traderequest_dict:
                #     print("  traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        quit()
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))

def get_order_close():
    print(" closing position #{}".format(result.order))
    #time.sleep(2)
    # create a close request
    position_id=result.order
    price=mt5.symbol_info_tick(symbol).bid
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "position": position_id,
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
    print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)
    else:
        print("4. position #{} closed, {}".format(position_id,result))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()



# get_order(side='buy',symbol='KO',lot=1.0)

