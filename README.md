# Super Simple Stock JP Morgan

Requirements
------------
Python 3.5

Assumptions
------------
1. Since Stock Price, Dividend, Index, Dividend Yield, P/E ratio can't be 0 in real
cases, we assumed that in case of missing data or error, value 0 shell be returned.
For example, if there is no trade records in give 15 minutes interval, 
Stock Price shell be 0 etc.

2. We assume that only synchronose usage of all objects and methods. If time is 
provided as optional argument (for debuging perpouses) it must always increase 
while code is executing, analogous to the real time.

Example Usage
-------------
```python
market = Market(900)
market.insert_stock("TEA", '1')
market.insert_stock("GIN", '1', '0.02')

stock_tea = market.get_stock("TEA")
stock_gin = market.get_stock("GIN")

stock_tea.record_dividend('3.20')
stock_tea.record_trade(Trade(Trade.buy, '10', '100'))
stock_gin.record_trade(Trade(Trade.buy, '13.45', '100'))
stock_tea.record_trade(Trade(Trade.buy, '11', '400'))
stock_gin.record_trade(Trade(Trade.buy, '16.77', '400'))
```