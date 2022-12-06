# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 12:31:02 2022

@author: User1
"""

import sys
import time
from datetime import timedelta
import datetime as dt
import JupitronAPI

import indicators as ta
import signal_generators as sg
import trade_generator as tg
import myutils
import strategystatus
import params


# user dependent
historical_data_path = '/DATA/NSE/Equity/'
TradeAccountParaFile = 'TradingAccount.txt'

# constants for status file
sscol_symbol = 0
sscol_trdsymbol = 1
sscol_symbolname = 2
sscol_entry_orderqty = 3
sscol_entry_orderprice = 4
sscol_entry_modifiedprice = 5
sscol_entry_filledqty = 6
sscol_entry_balanceqty = 7
sscol_entry_price = 8
sscol_entry_orderid = 9
sscol_entry_executing = 10
sscol_entry_signal = 11

sscol_exit_orderqty = 12
sscol_exit_orderprice = 13
sscol_exit_modifiedprice = 14
sscol_exit_filledqty = 15
sscol_exit_balanceqty = 16
sscol_exit_price = 17
sscol_exit_orderid = 18
sscol_exit_executing = 19
sscol_exit_reason = 20

# constants for scan list file
# API dependent
sclcol_symbol = 0
sclcol_trdsymbol = 1
sclcol_symbolname = 2
sclcol_lotsize = 7
sclcol_spotsymbol = 8


# scan interval in minutes
scan_interval = 5

# API dependent
spot_exchange = 'nse_cm' # NSE cash market
fo_exchange = 'nse_fo' # NSE derivatives market
orderduration = 'DAY'  # GTD / GFD or IOC

# define your own values based on your strategy
starttime = dt.time(9, 15, 0)
stoptime = dt.time(15, 15, 0)

stopalgo = False

def MACDScanner():
    
    try:
            
        # initialize the API, connect, login, etc
        jp = JupitronAPI.Jupitron()
        
        # Login
        lg = jp.Login('iiqfstudent', 'iiqf*#123')
        
        if (lg == None):
            print('Failed to connect to server')
            return
        elif (lg['Message'] != 'Login Successful'):
            print(lg)
            return
        else:
            print(lg)
        
        # get the trading account details
        userid, password, acountid = params.GetTradeAccountPara(TradeAccountParaFile)
        
        
        # strategy dependent
        # get the signal parameters
        short_period, long_period, long_entry, short_entry = params.GetSignalPara_MACD('MACDSignalParams.csv')
        
        # get the trade parameters
        capital, max_capital_deploy, buy_margin, sell_margin, pnl_target, pnl_stoploss, trading_cost = params.GetTradePara('MACDTradeParams.csv')
        
        # get the scan list
        # API dependent
        tradescanlist = myutils.read_dataframe('MACDScanList.csv')
        
        # get the strategy state
        strategy_state = myutils.read_dataframe('MACDStrategyState.csv')
        
        current_time = dt.datetime.now().time()
        
        if (current_time < starttime or current_time > stoptime ):
            return
        
        
        print('Starting algo system')
        
        stopalgo = False
        
        while (current_time < stoptime):
            print('Starting scan')
            
            for stocknum in range(len(tradescanlist)):
                stockname = tradescanlist.iloc[stocknum, sclcol_symbolname]
                
                print('\nChecking : ' + stockname)
                
                is_order_executing = strategy_state.iloc[stocknum, sscol_entry_executing] + strategy_state.iloc[stocknum, sscol_exit_executing] 
                
                if (is_order_executing == 0):
                    # no trades are currentlypending execution on this stock
                    
                    spotsymbol = str(tradescanlist.iloc[stocknum, sclcol_spotsymbol])
                    
                    # make API call to get live spot LTP
                    # API dependent
                    spotltp = jp.GetQuote(spot_exchange, spotsymbol)
                    
                    # API dependent
                    if (spotltp == None):
                        print('Error getting live spot price for ' + stockname)
                        stopalgo = True
                        break
                    # or
    #                if (spotltp == None):
    #                    print('Could not get LTP for ' + stockname)
    #                    continue
                    
                    # API dependent
                    spotltp = float(spotltp['LTP'])
                    
                    # user dependent
                    # todo
                    # optimize the code - keep historical data in memory
                    current_signal = sg.generate_signal_MACD(stockname, spotltp, short_period, long_period, long_entry, short_entry, historical_data_path)
                    
                    if (current_signal == None):
                        print('Signal generattion failed for ' + stockname)
                        continue
                    
                    print('Signal for '+ stockname + ' : ' + str(current_signal))
                    
                    # todo
                    # optimize the code so that on entry trade if there is no signal then it will skip to the next stock
                    
                    lotsize = tradescanlist.iloc[stocknum, sclcol_lotsize]
                    
                    # API dependent
                    futsymbol = str(tradescanlist.iloc[stocknum, sclcol_symbol])
                    
                    # make API call to get live Futures LTP
                    # API dependent
                    futltp = jp.GetQuote(fo_exchange, futsymbol)
                    
                    # API dependent
                    if (futltp == None):
                        print('Error getting live futures price for ' + stockname)
                        stopalgo = True
                        break
                    # or
    #                if (futltp == None):
    #                    print('Could not get futures LTP for ' + stockname)
    #                    continue
                    
                    # API dependent
                    futltp = float(futltp['LTP'])
                    
                    current_pos = strategy_state.iloc[stocknum, sscol_entry_filledqty] + strategy_state.iloc[stocknum, sscol_exit_filledqty] 
                    
                    prev_signal = strategy_state.iloc[stocknum, sscol_entry_signal]
                    
                    if (current_pos != 0):
                        # do MTM PL
                        
                        # we are as of now not taking into account partial executed exit trades while calculating the MTM PL
                        # todo later
                        
                        entryqty = strategy_state.iloc[stocknum, sscol_entry_filledqty]
                        entryprice = strategy_state.iloc[stocknum, sscol_entry_price]
                        mtm_pl = entryqty * (futltp - entryprice)
                        isentrytrade = False
                    else:
                        mtm_pl = 0
                        isentrytrade = True
                        strategystatus.ResetStrategyState(stocknum, strategy_state)
                    
                    if ((current_signal != 0)  ):
                        # if we have a signal
                        
                        prevexitreason  = ''
                        
                        orderqty, orderprice, exitreason = tg.generate_trade(futltp, current_signal, current_pos, prev_signal, 
                                                                          capital, max_capital_deploy, buy_margin, sell_margin,
                                                                          pnl_target, pnl_stoploss, mtm_pl, lotsize, prevexitreason)
                        
                        # Place the order in the exchange
                        if (orderqty > 0):
                            # place a BUY order
                            
                            # API dependent
                            trdsymbol = tradescanlist.iloc[stocknum, sclcol_trdsymbol]
                            
                            # API dependent
                            # exchange, tradesymbol, qty, price, B/S, accountid, orderduration
                            orderid = jp.PlaceOrder(fo_exchange, trdsymbol, orderqty, orderprice, 'B', acountid, orderduration)
                            
                            if (orderid != None):
                                # API dependent
                                orderid = orderid['GUIOrderID']
                            else:
                                print('Buy order on ' + stockname + ' could not be placed')
                                stopalgo = True
                                break
                                # or
                                # continue
                                
                            if (orderid != ''):
                                print('Order placed on ' + stockname + '. Order : BUY, Qty : '+ str(orderqty) +', Price : '+ str(orderprice))
                                
                                if (isentrytrade):
                                    # update the status file entry side cols
                                    strategystatus.UpdateStrategyState(isentrytrade, stocknum, orderqty, orderprice, 0.0, 0, 0.0, 
                                                                       orderid, 1, current_signal, 0, strategy_state, True)
                                else:
                                    # update the status file exit side cols
                                    strategystatus.UpdateStrategyState(isentrytrade, stocknum, orderqty, orderprice, 0.0, 0, 0.0, 
                                                                       orderid, 1, current_signal, 0, strategy_state, True)
                            else:
                                print('Buy order on ' + stockname + ' could not be placed')
                                stopalgo = True
                                break
                                # or
                                # continue
                                
                        elif (orderqty < 0):
                            # place a SELL order
                            
                            # API dependent
                            trdsymbol = tradescanlist.iloc[stocknum, sclcol_trdsymbol]
                            
                            # API dependent
                            # exchange, tradesymbol, qty, price, B/S, accountid, orderduration
                            orderid = jp.PlaceOrder(fo_exchange, trdsymbol, abs(orderqty), orderprice, 'S', acountid, orderduration)
                            
                            if (orderid != None):
                                # API dependent
                                orderid = orderid['GUIOrderID']
                            else:
                                print('Sell order on ' + stockname + ' could not be placed')
                                stopalgo = True
                                break
                                # or
                                # continue
                                
                            if (orderid != ''):
                                print('Order placed on ' + stockname + '. Order : SELL, Qty : '+ str(abs(orderqty)) +', Price : '+ str(orderprice))
                                
                                if (isentrytrade):
                                    # update the status file entry side cols
                                    strategystatus.UpdateStrategyState(isentrytrade, stocknum, orderqty, orderprice, 0.0, 0, 0.0, 
                                                                       orderid, 1, current_signal, 0, strategy_state, True)
                                else:
                                    # update the status file exit side cols
                                    strategystatus.UpdateStrategyState(isentrytrade, stocknum, orderqty, orderprice, 0.0, 0, 0.0, 
                                                                       orderid, 1, current_signal, 0, strategy_state, True)
                            else:
                                print('Sell order on ' + stockname + ' could not be placed')
                                stopalgo = True
                                break
                                # or
                                # continue
                        
    #                    else:
    #                        # if we dont have a qty to be trades=d
    #                        # do nothing
    #                        pass
                            
    #                else:
    #                    # if we dont have a signal
    #                    # do nothing
    #                    pass
    #                    
                else:
                    # if an order in currently executing on this stock, then check its status and update the status file
                    
                    if (isentrytrade):
                        orderid = strategy_state.iloc[stocknum, sscol_entry_orderid]
                        if (strategy_state.iloc[stocknum, sscol_entry_signal] == 'B'):
                            sgn = 1
                        else:
                            sgn = -1    
                    else:
                        orderid = strategy_state.iloc[stocknum, sscol_exit_orderid]
                        if (strategy_state.iloc[stocknum, sscol_entry_signal] == 'B'):
                            sgn = -1
                        else:
                            sgn = 1    
                        
                    # API dependent
                    orderstatus = jp.GetOrderStatus(orderid)
                    
                    if (orderstatus == None):
                        continue
                    
                    status = orderstatus['OrdStatus']
                    # API dependent
                    
                    if (status == 'complete'):
                        # API dependent
                        print('Order complete : ' + strategy_state.iloc[stocknum, sscol_symbolname] + ' Trade : ' + orderstatus['TransType'] + ' Filled : ' + orderstatus['FilledShares'])
                        
                        strategystatus.UpdateStrategyState(isentrytrade, stocknum, int(orderstatus['QuanToFill']), 0, 0.0, 
                                                           sgn * int(orderstatus['FilledShares']), orderstatus['AvgPrice'], 0, 0, 0, exitreason, 
                                                           strategy_state, False)
                    elif (status == 'rejected'):
                        # API dependent
                        print('Order rejected : ' + strategy_state.iloc[stocknum, sscol_symbolname] + ' Trade : ' + orderstatus['TransType'] + ' Filled : ' + orderstatus['FilledShares'])
                        
                        strategystatus.UpdateStrategyState(isentrytrade, stocknum, int(orderstatus['QuanToFill']), 0, 0.0, 
                                                           sgn * int(orderstatus['FilledShares']), orderstatus['AvgPrice'], 0, 0, 0, exitreason, 
                                                           strategy_state, False)
                    elif (status == 'cancelled'):
                        # API dependent
                        print('Order cacelled : ' + strategy_state.iloc[stocknum, sscol_symbolname] + ' Trade : ' + orderstatus['TransType'] + ' Filled : ' + orderstatus['FilledShares'])
                        
                        strategystatus.UpdateStrategyState(isentrytrade, stocknum, int(orderstatus['QuanToFill']), 0, 0.0, 
                                                           sgn * int(orderstatus['FilledShares']), orderstatus['AvgPrice'], 0, 0, 0, exitreason, 
                                                           strategy_state, False)
                    elif (status == 'open'):
                        # API dependent
                        print('Order open : ' + strategy_state.iloc[stocknum, sscol_symbolname] + ' Trade : ' + orderstatus['TransType'] + ' Filled : ' + orderstatus['FilledShares'])
                        
                        strategystatus.UpdateStrategyState(isentrytrade, stocknum, int(orderstatus['QuanToFill']), 0, 0.0, 
                                                           sgn * int(orderstatus['FilledShares']), orderstatus['AvgPrice'], 0, 1, 0, exitreason, 
                                                           strategy_state, False)
                        
                        # todo later
                        # modify order price if there is adverse price movement
                        
            # end of for loop scanning through the scan list
            
            # write the strategy state file to disk
            myutils.write_dataframe('MACDStrategyState.csv', strategy_state)
            
            print('Ended scan')
            
            if (stopalgo == True):
                print('Some error has forced stop the algo')
                break
            
            current_time = dt.datetime.now().time()
            if (current_time > stoptime ):
                break
            
            time.sleep(scan_interval * 60)
        
        # end of the while loop
        
        # algo exited the while loop
        
        print('Algo stopped for the day')
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None

    
MACDScanner()
