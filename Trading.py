from collections import deque
from decimal import Decimal  # to provide sufficient accuracy for financial arithmetic
import datetime


class Trade(object):
    buy = 0
    sell = 1

    def __init__(self, indicator, price, quantity):
        if price <= 0 or quantity <= 0 or (indicator != Trade.buy and indicator != Trade.sell):
            raise ValueError
        self.indicator = indicator
        self.quantity = quantity
        self.price = price


class Stock(object):

    def __init__(self, stock_symbol, trades_expiry_time):
        self.stock_symbol = stock_symbol
        self.last_trades = deque()
        self.sum = Decimal(0)
        self.volume = Decimal(0)
        self.full_history = []
        self.trades_expiry_time = trades_expiry_time

    def __add_trade(self, trade, t):
        """
        Low level method for adding trade to deque
        :param trade: Trade object
        :param ts: [datatime.datatime]
        :return: None
        """

        self.last_trades.append((t, trade))
        self.full_history.append((t, trade))
        self.sum += Decimal(trade.price) * Decimal(trade.quantity)
        self.volume += Decimal(trade.quantity)

    def __remove_oldest_trade(self):
        """
        Low level method for removing the oldest trade
        :return: None
        """
        (_, trade) = self.last_trades.popleft()
        self.sum -= Decimal(trade.price) * Decimal(trade.quantity)
        self.volume -= Decimal(trade.quantity)

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
