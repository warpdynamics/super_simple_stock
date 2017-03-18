# Super Simple Stock JP Morgan

Requirements
------------
Python 3.5

Instalation
-----------
```bash
pip install super_simples_stock -e
```

Assumptions
------------
1. Since Stock Price, Dividend, Index, Dividend Yield, P/E ratio can't be 0 in real
cases, we assumed that in case of missing data or error, value 0 shell be returned.
For example, if there is no trade records in give 15 minutes interval, 
Stock Price shell be 0 etc.

2. We assumed only synchronous usage of all objects and methods. If time is 
provided as optional argument (for debuging perpouses) it must always increase 
while code is executing, analogous to the real time.

Example Usage
-------------
```python
market = Market(trades_expiry_time=900)
market.insert_stock(stock_symbol="TEA", par_value='1')
market.insert_stock(stock_symbol="GIN", par_value='1', fixed_dividen='0.02')

stock_tea = market.get_stock(stock_symbol="TEA")
stock_gin = market.get_stock(stock_symbol="GIN")

stock_tea.record_dividend(value='3.20')
stock_tea.record_trade(trade=Trade(indicator=Trade.buy, price='10', quantity='100'))
stock_gin.record_trade(trade=Trade(indicator=Trade.buy, price='13.45', quantity='100'))
stock_tea.record_trade(trade=Trade(indicator=Trade.buy, price='11', quantity='400'))
stock_gin.record_trade(trade=Trade(indicator=Trade.buy, price='16.77', quantity='400'))

print(stock_gin.get_price())
print(stock_gin.divided_yield())
print(market.get_index())
```