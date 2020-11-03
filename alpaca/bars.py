import config, requests, json
import datetime as dt

holdings = open('data\QQQ.csv').readlines()
symbols = [holding.split(',')[2].strip() for holding in holdings][1:]
symbols = ",".join(symbols)
limit_bars = 1000

minute_bars_url = config.BARS_URL + '/5Min?symbols=MSFT&limit=' + str(limit_bars)
day_bars_url = '{}/day?symbols={}&limit='.format(config.BARS_URL, symbols, str(limit_bars))
r = requests.get(day_bars_url, headers=config.HEADERS)

data = r.json()
#print(json.dumps(r.json(), indent=4))

# type in the console:
# python bars.py > output.txt

for symbol in data:
    filename = 'data/ohlc/{}.txt'.format(symbol)
    x = open(filename, 'w+')
    x.write('Date,Open,High,Low,Close,Volume,OpenInterest\n')
    for bar in data[symbol]:
        #t = dt.datetime.fromtimestamp(bar['t'])
        #day = t.strftime('%Y-%m-%d')
        line = '{},{},{},{},{},{},{}\n'.format(bar['t'],bar['o'],bar['h'],bar['l'],bar['c'],bar['v'], 0.00)
        x.write(line)