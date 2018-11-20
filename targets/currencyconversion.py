import requests
from decimal import Decimal

class CurrencyHDP(object):
    symbol = 'USD'
    time = 0
    avgPrice = 0

    def __init__(self, time, targetCurrency):
        self.time = time.strftime('%s')
        self.symbol = targetCurrency
        self.initiate()

    def initiate(self):
        uri = 'https://min-api.cryptocompare.com'
        path = '/data/histohour'
        queryStr = "?fsym=XMR&tsym={tsym}&limit=1&e=CCCAGG&toTs={time}".format(tsym=self.symbol, time=self.time)
        url = uri + path + queryStr
        r = requests.get(url)
        hdp = r.json()["Data"][1]
        self.avgPrice = Decimal((hdp["high"] + hdp["low"]) / 2)

    def convert(self, amount):
        return (self.avgPrice*amount)