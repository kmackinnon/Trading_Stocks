# usr/bin/python27

import csv
import ystockquote #retrieve stock quote data from Yahoo Finance

"""
with open('targets.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
"""

r = csv.reader(open('targets.csv', 'rb'))
#w = csv.writer(open('targets.csv', 'a'))


def addStock(stock, price):
    with open ('targets.csv', 'a') as w:
        writer = csv.writer(w)
        writer.writerow([stock] + [price])
    
def deleteStock(stock):
    #If the user wishes to edit the csv file, he may do so here
    pass
                     
def main():
    while True:
        enterMore = raw_input("Add more stocks to watchlist? (y/n) ")[:1].lower()
        if enterMore == 'y':
            stock = raw_input("Enter stock: ")
            price = raw_input("Enter price: ")
            addStock(stock, price)
        elif enterMore == 'n':
            for line in r:
                price = ystockquote.get_price(line[0])
                sma50 = ystockquote.get_50day_moving_avg(line[0])
                sma200 = ystockquote.get_200day_moving_avg(line[0])
                if line[1] <= price:
                    opportunity = 'BUY'
                else:
                    opportunity = ''
                print ', '.join(line), price, opportunity
            break
        else:
            break

if __name__ == '__main__':
    main()
