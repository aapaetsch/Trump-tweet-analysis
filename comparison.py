import yfinance as yf
import json
import datetime
from math import log10


def test2():
	data = getStock('^GSPC', 'max')
	x = data.loc['2019-12-30']['Close']
	y = data.loc['2019-12-31']['Close']
	diff = y-x
	print(diff)

def comparison(tweets, marketData):
	uniqueGrams = {}

def sortTweets(allTweets):
	sortedTweets = {} #K = date, v = list of tweets for that day






def getStock(ticker, p):
	return yf.Ticker(ticker).history(period=p)


def test():

	print('S&P')
	sp = yf.Ticker('^GSPC')
	print(sp.history(period='max'))

	print("Nasdaq")
	nasdaq = yf.Ticker('^IXIC')
	print(nasdaq.history(period="max"))

	print("Dow Jones")
	dji = yf.Ticker('^DJI')
	print(dji.history(period='max'))

# if __name__ is "__main__":
# 	test()
 

test2()
