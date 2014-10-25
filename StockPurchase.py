# usr/bin/python27

import pprint
import time
import threading
import sqlite3
import ystockquote

conn = sqlite3.connect('price.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS stocks (ticker, target_price, true_price)''')

def format_print(object, context, maxlevels, level):
    typ = pprint._type(object)
    if typ is unicode:
        object = str(object)
    return pprint._safe_repr(object, context, maxlevels, level)

def add_stock(stock, target):
    price = ystockquote.get_price(stock)
    c.execute("INSERT INTO stocks VALUES (?,?,?)", (stock, target, price,))
    conn.commit() # Save (commit) the changes
    print "\nStock added to database"

def validate_stock(stock):
    return ystockquote.get_price(stock) != "0.00"

def remove_stock(stock):
    c.execute('''DELETE FROM stocks WHERE stock = ?''',stock)

def print_watched_stocks():
    pp = pprint.PrettyPrinter()
    pp.format = format_print(object, context, maxlevels, level)

    for row in c.execute("SELECT * FROM stocks ORDER BY true_price"):
        pp.pprint(row)
                     
def main():
    print "\nUsage: close the program by typing q"
    cmd = raw_input("\nAdd more stocks to watchlist? (y/n) ")[:1].lower()

    while cmd != 'q':
        
        if cmd == 'y':
            stock = raw_input("Enter stock: ")
            target = raw_input("Enter price: ")

            if validate_stock(stock):
                add_stock(stock, target)
            else:
                print "Invalid stock. Please enter a valid ticker"

        elif cmd == 'n':
            cmd = raw_input("\nRemove any stocks from watchlist? (y/n) ")[:1].lower()
            
            if cmd == 'y':
                stock = raw_input("Enter stock: ")
                remove_stock(stock)
            elif cmd == 'n':
                print_watched_stocks()
                break
            else:
                continue;

        else:
            print_watched_stocks()
            conn.close() # Close the connection
            break

        cmd = raw_input("\nAdd more stocks to watchlist? (y/n) ")[:1].lower()

if __name__ == '__main__':
    main()
