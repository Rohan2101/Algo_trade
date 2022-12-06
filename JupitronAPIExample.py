# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 10:30:18 2020

@author: User1
"""

import time
import csv

# import the Jupitron API Library
import JupitronAPI


# Create a Jupitron object
jp = JupitronAPI.Jupitron()


# Login
lg = jp.Login('iiqfstudent', 'iiqf*#123')

if (lg == None):
    print('Failed to connect to server')
elif (lg['Message'] != 'Login Successful'):
    print(lg)
else:
    print(lg)

# Get the live market prices of NIFTY spot
niftyspotsymbol = '26000'
niftyspot = jp.GetQuote('nse_cm', niftyspotsymbol)
print(niftyspot)


# Get the live market prices of BANKNIFTY spot
bankniftyspotsymbol = '26009'
bankniftyspot = jp.GetQuote('nse_cm', bankniftyspotsymbol)
print(bankniftyspot)


# Get the live market prices of ACC spot
stocksymbol = '22'
stockprice = jp.GetQuote('nse_cm', stocksymbol)
print(stockprice)

ltp = float(stockprice['LTP'])
print(ltp)


# Get the live market OHLC prices
ohlc = jp.GetOHLC('nse_cm', stocksymbol)
print(ohlc)

# Get the live market 5-depth OrderBook quotes
orderbook = jp.GetOrderBookQuote('nse_cm', stocksymbol)
print(orderbook)

# Place a BUY order
order = jp.PlaceOrder('nse_cm', 'ACC-EQ', 10, ltp-100, 'B', 'TEST89', 'DAY' )
print(order)

if (order != None):
    orderID = order['GUIOrderID']
else:
    orderID = ''
    
# Get the status of a placed order
orderStatus = jp.GetOrderStatus(orderID)
print(orderStatus)

NestorderID = orderStatus['NestOrdNum']


# Modify an OPEN order
# Exchange, GUIOrderID, OrderQty, OrderPrice, OrderValidity = 'DAY', OrderPriceType = 'L'
modstatus = jp.ModifyOrder(orderID, NestorderID, 'nse_cm', 10, ltp-90)
print(modstatus)

# Cancel an OPEN order
#cncstatus = jp.CancelOrder(orderID, NestorderID)
#print(cncstatus)


# Get the status of all the orders placed during the day
orderHistory = jp.GetOrderHistory()
print(orderHistory)

# Get the status of all the executed trades during the day
tradeHistory = jp.GetTradeHistory()
print(tradeHistory)


# scan the live prices of a stock every 1 second
stocksymbol = '22'
for i in range(10):
    q = jp.GetQuote('nse_cm', stocksymbol)
    print(q['LTP'])
    time.sleep(1)
    

# get nse cash segment master data
nse_cash_master = jp.GetMasterData('nse_cm')

# get nse F&O segment master data
nse_fo_master = jp.GetMasterData('nse_fo')



def write_data(file_name, data):
    myfile = open(file_name, 'w')
    with myfile:
        writer = csv.writer(myfile, lineterminator = '\n')
        
        for row in data:
            writer.writerow(row.split(','))
            
        myfile.close()


write_data('nse_cm_master.csv',nse_cash_master)
write_data('nse_fo_master.csv',nse_fo_master)



# Derivatives Trade Example
symbol = '48738'
price = jp.GetQuote('nse_fo', symbol)
print(price)

ltp = float(q['LTP'])

order = jp.PlaceOrder('nse_fo', 'BANKNIFTY21SEPFUT', 25, ltp, 'B', 'TEST89', 'DAY' )
orderID = order['GUIOrderID']

orderStatus = jp.GetOrderStatus(orderID)
print(orderStatus)

order = jp.PlaceOrder('nse_fo', 'BANKNIFTY21SEPFUT', 25, ltp-10, 'S', 'TEST89', 'DAY' )
orderID = order['GUIOrderID']

orderStatus = jp.GetOrderStatus(orderID)
print(orderStatus)

NestorderID = orderStatus['NestOrdNum']

# Modify an OPEN order
# Exchange, GUIOrderID, OrderQty, OrderPrice, OrderValidity = 'DAY', OrderPriceType = 'L'
modstatus = jp.ModifyOrder(orderID, NestorderID, 'nse_fo', 10, ltp-90)
print(modstatus)

# Cancel an OPEN order
#cncstatus = jp.CancelOrder(orderID, NestorderID)
#print(cncstatus)


