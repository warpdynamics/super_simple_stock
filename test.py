from trading import Trade, Stock, Market
from datetime import datetime
from decimal import Decimal
import random
import math

import unittest


def ts(t):
    return datetime.fromtimestamp(t)


class Test(unittest.TestCase):

    def test_stocks1(self):
        stock = Stock("TEA", 900, '1')
        stock.record_dividend('3.20')
        stock.record_trade(Trade(Trade.buy, '10', '100'), ts(0))
        stock.record_trade(Trade(Trade.buy, '11', '400'), ts(200))
        self.assertEqual(stock.get_price(ts(200)), Decimal('10.8'))
        stock.record_trade(Trade(Trade.buy, '12', '400'), ts(1000))
        self.assertEqual(stock.get_price(ts(1001)), Decimal('11.5'))
        self.assertEqual(round(stock.dividend_yield(ts(1001)), 4), Decimal('0.2783'))
        self.assertEqual(stock.get_price(ts(1800)), Decimal('12'))
        self.assertEqual(round(stock.dividend_yield(ts(1800)), 4), Decimal('0.2667'))
        self.assertEqual(stock.get_price(ts(2000)), Decimal('0'))
        self.assertEqual(stock.dividend_yield(ts(2000)), Decimal('0'))

        stock = Stock("GIN", 900, '1', '0.02')
        stock.record_trade(Trade(Trade.buy, '13.45', '100'), ts(0))
        stock.record_trade(Trade(Trade.buy, '16.77', '400'), ts(200))
        self.assertEqual(stock.get_price(ts(200)), Decimal('16.106'))
        stock.record_trade(Trade(Trade.buy, '12.01', '711'), ts(1000))
        self.assertEqual(round(stock.get_price(ts(1001)), 4), Decimal('13.7238'))
        self.assertEqual(round(stock.dividend_yield(ts(1001)), 4), Decimal('0.0015'))
        self.assertEqual(stock.get_price(ts(1800)), Decimal('12.01'))
        self.assertEqual(round(stock.dividend_yield(ts(1800)), 4), Decimal('0.0017'))
        self.assertEqual(stock.get_price(ts(2000)), Decimal('0'))
        self.assertEqual(stock.dividend_yield(ts(2000)), Decimal('0'))

    def test_stocks2(self):
        expire = 900
        stock = Stock("TEA", expire, '1')
        tracker = []
        for T in range(0, 2000):
            val = Decimal(10 + random.random())
            qty = Decimal(random.randint(100, 200))
            tracker.append((T, val, qty))
            trade = Trade(Trade.buy, val, qty)
            stock.record_trade(trade, ts(T))
            price1 = stock.get_price(ts(T))

            filtered = list(filter(lambda k: T - k[0] <= expire, tracker))
            price2 = sum(map(lambda k: k[1]*k[2], filtered))/sum(map(lambda k: k[2], filtered))

            self.assertAlmostEqual(price1, price2)

    def test_market(self):
        market = Market(900)
        market.insert_stock("TEA", '1')
        market.insert_stock("GIN", '1', '0.02')

        stock_tea = market.get_stock("TEA")
        stock_gin = market.get_stock("GIN")

        stock_tea.record_dividend('3.20')
        stock_tea.record_trade(Trade(Trade.buy, '10', '100'), ts(0))
        stock_gin.record_trade(Trade(Trade.buy, '13.45', '100'), ts(100))
        stock_tea.record_trade(Trade(Trade.buy, '11', '400'), ts(200))
        stock_gin.record_trade(Trade(Trade.buy, '16.77', '400'), ts(500))

        self.assertEqual(stock_tea.get_price(ts(600)), Decimal('10.8'))
        self.assertEqual(stock_gin.get_price(ts(600)), Decimal('16.106'))

        self.assertAlmostEqual(market.get_index(ts(600)), math.sqrt(Decimal('10.8')*Decimal('16.106')))

    def test_market_no_ts(self):
        market = Market(900)
        market.insert_stock(stock_symbol="TEA", par_value='1')
        market.insert_stock(stock_symbol="GIN", par_value='1', fixed_dividen='0.02')

        stock_tea = market.get_stock(stock_symbol="TEA")
        stock_gin = market.get_stock(stock_symbol="GIN")

        stock_tea.record_dividend(value='3.20')
        stock_tea.record_trade(trade=Trade(indicator=Trade.buy, price='10', quantity='100'))
        stock_gin.record_trade(trade=Trade(indicator=Trade.buy, price='13.45', quantity='100'))
        stock_tea.record_trade(trade=Trade(indicator=Trade.buy, price='11', quantity='400'))
        stock_gin.record_trade(trade=Trade(indicator=Trade.buy, price='16.77', quantity='400'))

        self.assertEqual(stock_tea.get_price(), Decimal('10.8'))
        self.assertAlmostEqual(stock_tea.dividend_yield(), Decimal('3.20')/Decimal('10.8'))
        self.assertEqual(stock_gin.get_price(), Decimal('16.106'))
        self.assertAlmostEqual(stock_gin.dividend_yield(), Decimal('0.02')/Decimal('16.106'))

        self.assertAlmostEqual(market.get_index(), math.sqrt(Decimal('10.8')*Decimal('16.106')))

if __name__ == '__main__':
    unittest.main()
