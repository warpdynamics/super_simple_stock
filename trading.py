from collections import deque
from decimal import Decimal  # to provide sufficient accuracy for financial arithmetic
import datetime
import math


class Trade(object):
    buy = 0
    sell = 1

    def __init__(self, indicator, price, quantity):
        price = Decimal(price)
        quantity = Decimal(quantity)
        if price <= 0 or quantity <= 0 or (indicator != Trade.buy and indicator != Trade.sell):
            raise ValueError
        self.indicator = indicator
        self.quantity = quantity
        self.price = price


class Stock(object):
    """
    class Stock is representing a single stock
    """

    def __init__(self, stock_symbol, trades_expiry_time, par_value, fixed_dividen=None):
        """
        :param stock_symbol: string stock symbol
        :param trades_expiry_time: how long trades should be remember to calculate share price is seconds [int]
        :param par_value: Par Value in given currency units e.g in GBP [string]
        :param fixed_dividen: [string]
        :return: None
        """
        self.stock_symbol = stock_symbol
        self.last_trades = deque()
        self.sum = Decimal(0)
        self.volume = Decimal(0)
        self.trades_expiry_time = trades_expiry_time
        self.par_value = Decimal(par_value)
        if fixed_dividen is not None:
            self.fixed_dividend = Decimal(fixed_dividen)
        else:
            self.fixed_dividend = None
        self.last_dividend = Decimal(0)

    def __add_trade(self, trade, t):
        """
        Low level method for adding trade to deque
        :param trade: Trade object
        :param ts: [datatime.datatime]
        :return: None
        """

        self.last_trades.append((t, trade))
        self.sum += trade.price * trade.quantity
        self.volume += trade.quantity

    def __remove_oldest_trade(self):
        """
        Low level method for removing the oldest trade
        :return: None
        """
        (_, trade) = self.last_trades.popleft()
        self.sum -= trade.price * trade.quantity
        self.volume -= trade.quantity

    def __clean_last_trades(self, t):
        while len(self.last_trades) > 0:
            (oldest_t, _) = self.last_trades[0]
            if (t - oldest_t).total_seconds() > self.trades_expiry_time:
                self.__remove_oldest_trade()
            else:
                break

    def record_trade(self, trade, t=None):
        """
        :param trade: Trade object
        :param t: optional, for test use
        :return: None
        """
        if t is None:
            t = datetime.datetime.utcnow()

        self.__add_trade(trade, t)
        self.__clean_last_trades(t)

    def get_price(self, t=None):
        """
        :param t: optional, for test use
        :return: price
        """
        if t is None:
            t = datetime.datetime.utcnow()
        self.__clean_last_trades(t)
        if len(self.last_trades) == 0:
            return Decimal(0)
        return self.sum/self.volume

    def record_dividend(self, value):
        """
        :param value: value of dividend in given currency units e.g in GBP [string]
        :return: None
        """
        self.last_dividend = Decimal(value)

    def dividend_yield(self, t=None):
        price = self.get_price(t)

        if price == 0:
            return Decimal(0)

        if self.fixed_dividend is None:
            return self.last_dividend/price
        else:
            return (self.fixed_dividend * self.par_value)/price

    def get_pe_ratio(self, t=None):
        price = self.get_price(t)
        if self.last_dividend == 0:
            return Decimal(0)

        return price/self.last_dividend


class Market(object):
    def __init__(self, trades_expiry_time):
        self.stocks = {}
        self.trades_expiry_time = trades_expiry_time

    def insert_stock(self, stock_symbol, par_value, fixed_dividen=None):
        stock = Stock(stock_symbol, self.trades_expiry_time, par_value, fixed_dividen)
        if stock.stock_symbol in self.stocks:
            raise ValueError("This Stock is already in the market")

        self.stocks[stock.stock_symbol] = stock

    def get_stock(self, stock_symbol):
        if stock_symbol in self.stocks:
            return self.stocks[stock_symbol]
        else:
            return None

    def get_index(self, t=None):
        if len(self.stocks) == 0:
            return 0
        if t is None:
            t = datetime.datetime.utcnow()
        try:
            #  as we expect rather thousands of stocks,
            #  to not lose precision we've chosen to calculate arithmetic mean from logarithms and then return exponent
            #  from the result.
            logs = [math.log(self.get_stock(stock_symbol).get_price(t)) for stock_symbol in self.stocks]
            return math.exp(sum(logs)/float(len(self.stocks)))
        except ValueError:
            return 0
