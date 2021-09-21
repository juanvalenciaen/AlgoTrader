import pandas as pd
from dateutil.relativedelta import relativedelta
import dateutil.parser
import pytz
import math
import datetime as dt

def get_data_binance(symbol='BTCUSDT', start_time='2021-03-03', end_time='2021-03-04',interval_mins=60):

    # end_time = dt.date.today()
    # n_days = dt.timedelta(days=1)
    # start_time = end_time - n_days

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


get_data_binance()