# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 11:36:10 2022

@author: User1
"""

import sys


def generate_trade(ltp, current_signal, current_qty, prev_signal, capital, max_capital_deploy, buy_margin, sell_margin,
                   pnl_target, pnl_stoploss, mtm_pnl, lot_size, previous_exit_reason):
    
    # max_capital_deploy, buy_margin, sell_margin are in decimals
    # pnl_stoploss should be a +ve number
    
    try:
        
        if type(ltp) is str:
            ltp = float(ltp.strip())

        if ( ltp <= 0 ):
            print(ltp)
            print(sys._getframe().f_code.co_name,'Invalid parameter values0')
            return None, None, None
        
        if type(current_signal) is str:
            current_signal = int(current_signal.strip())
        
        if ( current_signal != 0 and current_signal != 1 and current_signal != -1 ):
            print(sys._getframe().f_code.co_name,'Invalid parameter values1')
            return None, None, None
        
        if type(current_qty) is str:
            current_qty = int(current_qty.strip())
        
        if type(prev_signal) is str:
            prev_signal = int(prev_signal.strip())
            
        if ( prev_signal != 0 and prev_signal != 1 and prev_signal != -1 ):
            print(sys._getframe().f_code.co_name,'Invalid parameter values2')
            return None, None, None
        
        if type(capital) is str:
            capital = float(capital.strip())

        if ( capital < 1 ):
            print(sys._getframe().f_code.co_name,'Invalid parameter values3')
            return None, None, None
        
        if type(max_capital_deploy) is str:
            max_capital_deploy = float(max_capital_deploy.strip())
        
        if ( max_capital_deploy <= 0 or max_capital_deploy > 1 ):
            print(sys._getframe().f_code.co_name,'Invalid parameter values4')
            return None, None, None

        if type(buy_margin) is str:
            buy_margin = float(buy_margin.strip())
        
        if ( buy_margin <= 0 or buy_margin > 1 ):
            print(sys._getframe().f_code.co_name,'Invalid parameter values5')
            return None, None, None
        
        if type(sell_margin) is str:
            sell_margin = float(sell_margin.strip())
        
        if ( sell_margin <= 0 or sell_margin > 1 ):
            print(sys._getframe().f_code.co_name,'Invalid parameter values6')
            return None, None, None
        
        if type(pnl_target) is str:
            pnl_target = float(pnl_target.strip())
        
        if type(pnl_stoploss) is str:
            pnl_stoploss = float(pnl_stoploss.strip())
        
        if type(mtm_pnl) is str:
            pnl_stoploss = float(mtm_pnl.strip())
        
        if type(lot_size) is str:
            lot_size = int(lot_size.strip())
        
        if ( lot_size < 1 ):
            print(sys._getframe().f_code.co_name,'Invalid parameter values7')
            return None, None, None
        
        
        orderqty = 0
        orderprice = 0.0
        exitreason = ''
        
        if (current_qty == 0):
            # if there is no existing open position
            
            # check for short signal
            if (current_signal == -1):
                # take a short pos
                orderprice = ltp
                
                margin_blocked = capital * max_capital_deploy
                
                orderqty = -(((margin_blocked // (orderprice * sell_margin)) // lot_size) * lot_size)
                
                if (abs(orderqty) < 1):
                    orderprice = 0.0
                
            # check for long signal
            elif (current_signal == 1):
                # take a long pos
                orderprice = ltp
                
                margin_blocked = capital * max_capital_deploy
                
                orderqty = ((margin_blocked // (orderprice * buy_margin)) // lot_size) * lot_size
                
                if (orderqty < 1):
                    orderprice = 0.0
                
            else:
                pass
            
        elif (current_qty != 0):
            # if there are existing open positions
            # check for exit conditions
            
            if (mtm_pnl > pnl_target):
                orderprice = ltp
                orderqty = -current_qty
                exitreason = 'TG'
            elif (mtm_pnl < -pnl_stoploss):
                orderprice = ltp
                orderqty = -current_qty
                exitreason = 'SL'
            elif (current_signal != prev_signal):
                orderprice = ltp
                orderqty = -current_qty
                exitreason = 'SC'

        return orderqty, orderprice, exitreason
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None, None, None

    
    
