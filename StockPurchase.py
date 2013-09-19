# usr/bin/python27

"""
I often find myself wanting a quick tool to determine whether I should invest in a particular stock.
The purpose of this application is to keep track of stocks in which you're interested.

To begin, the user enters a target price for a given stock.
If the market value goes below that price, the user may decide to purchase that stock.
There is also the added test of simple moving averages.
The idea is that if the more recent MA crosses the longer term MA from below, 
the stock should continue upwards (at least over the short term).
"""

import csv
import math
import ystockquote #retrieve stock quote data from Yahoo Finance

ERROR = 0.01 # 1% error

r = csv.reader(open('targets.csv', 'r'))
#w = csv.writer(open('targets.csv', 'a'))

# user adds stocks to the csv file
def addStock(stock, price):
    with open ('targets.csv', 'a') as w:
        writer = csv.writer(w)
        writer.writerow([stock] + [price])
    
# If the user wishes to edit the csv file, he may do so here    
def deleteStock(stock):
    pass

# buy if the market price is <= the target price
def isBuy(priceEntered, priceMarket):
    return priceMarket <= priceEntered

# a buy signal is triggered when the 50-day sma crosses the 200-day sma from below
def isCrossOver(sma50, sma200, quote):
    difference = sma50 - sma200
    return math.fabs(difference) < ERROR * quote
                     
def main():
    while True:
        enterMore = raw_input("\nAdd more stocks to watchlist? (y/n) ")[:1].lower()
        if enterMore == 'y':
            stock = raw_input("Enter stock: ")
            price = raw_input("Enter price: ")
            addStock(stock, price)
        elif enterMore == 'n':
            
            for line in r:
                try:
                    quote = float(ystockquote.get_price(line[0]))
                    sma50 = float(ystockquote.get_50day_moving_avg(line[0]))
                    sma200 = float(ystockquote.get_200day_moving_avg(line[0]))
                except ValueError:
                    print 'EOF'
                    break
                
                if isBuy(float(line[1]), quote): # if target less than market price, then purchase
                    opportunity = 'Current price under target. BUY'
                elif isCrossOver(quote, sma50, sma200): # if crossover from below, then purchase
                    opportunity = 'Possible crossover. BUY'
                else:
                    opportunity = ''
                print ', '.join(line), quote, opportunity
            
            break
        else:
            break

if __name__ == '__main__':
    main()
