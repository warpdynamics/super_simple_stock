# Super Simple Stock JP Morgan

Requirements
------------
Python 3.5

Assumptions
------------
Since Stock Price, Dividend, Index, Dividend Yield, P/E ratio can't be 0 in real
cases, we assumed that in case of missing data or error value 0 shell be returned.
For example, if there is no trade records in give 15 minutes interval, 
Stock Price shell be 0 etc.