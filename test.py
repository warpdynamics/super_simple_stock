from trading import Trade, Stock
from datetime import datetime
from decimal import Decimal

import unittest


def ts(t):
    return datetime.fromtimestamp(t)


class Test(unittest.TestCase):

    def test_stocks(self):
        stock = Stock("USD", 900)
        stock.record_trade(Trade(Trade.buy, Decimal('10'), Decimal('100')), ts(0))
        stock.record_trade(Trade(Trade.buy, Decimal('11'), Decimal('400')), ts(200))
        self.assertEqual(stock.get_price(ts(200)), Decimal('10.8'))
        stock.record_trade(Trade(Trade.buy, Decimal('12'), Decimal('400')), datetime.fromtimestamp(1000))
        self.assertEqual(stock.get_price(ts(1001)), Decimal('11.5'))
        self.assertEqual(stock.get_price(ts(1800)), Decimal('12'))
        self.assertEqual(stock.get_price(ts(2000)), Decimal('0'))

if __name__ == '__main__':
    unittest.main()
