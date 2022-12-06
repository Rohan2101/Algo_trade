# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 11:45:19 2022

@author: User1
"""

import sys



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


def UpdateStrategyState(isentrytrade, stocknum, orderqty, orderprice, modifiedprice, filledqty, tradeprice, orderid, isorderexecuting,
                        signal, exitreason, strategy_state, isneworder = True):
    
    try:
        if (isentrytrade):
            if (isneworder):
                strategy_state.iloc[stocknum, sscol_entry_orderqty] = orderqty
                strategy_state.iloc[stocknum, sscol_entry_orderprice] = orderprice
                strategy_state.iloc[stocknum, sscol_entry_signal] = signal
                strategy_state.iloc[stocknum, sscol_entry_orderid] = orderid
            else:
                strategy_state.iloc[stocknum, sscol_entry_modifiedprice] = modifiedprice
                
            strategy_state.iloc[stocknum, sscol_entry_filledqty] = filledqty
            strategy_state.iloc[stocknum, sscol_entry_balanceqty] = orderqty - filledqty
            strategy_state.iloc[stocknum, sscol_entry_price] = tradeprice
            strategy_state.iloc[stocknum, sscol_entry_executing] = isorderexecuting
            
        else:
            if (isneworder):
                strategy_state.iloc[stocknum, sscol_exit_orderqty] = orderqty
                strategy_state.iloc[stocknum, sscol_exit_orderprice] = orderprice
                strategy_state.iloc[stocknum, sscol_exit_orderid] = orderid
            else:
                strategy_state.iloc[stocknum, sscol_exit_modifiedprice] = modifiedprice
                
            strategy_state.iloc[stocknum, sscol_exit_filledqty] = filledqty
            strategy_state.iloc[stocknum, sscol_exit_balanceqty] = orderqty - filledqty
            strategy_state.iloc[stocknum, sscol_exit_price] = tradeprice
            strategy_state.iloc[stocknum, sscol_exit_executing] = isorderexecuting
            strategy_state.iloc[stocknum, sscol_exit_reason] = exitreason
            
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None
    
def ResetStrategyState(stocknum, strategy_state):
    
    try:
        strategy_state.iloc[stocknum, sscol_entry_orderqty] = 0
        strategy_state.iloc[stocknum, sscol_entry_orderprice] = 0
        strategy_state.iloc[stocknum, sscol_entry_signal] = 0
        strategy_state.iloc[stocknum, sscol_entry_orderid] = 0
        strategy_state.iloc[stocknum, sscol_entry_orderprice] = 0
        strategy_state.iloc[stocknum, sscol_entry_filledqty] = 0
        strategy_state.iloc[stocknum, sscol_entry_balanceqty] = 0
        strategy_state.iloc[stocknum, sscol_entry_price] = 0
        strategy_state.iloc[stocknum, sscol_entry_executing] = 0

        strategy_state.iloc[stocknum, sscol_exit_orderqty] = 0
        strategy_state.iloc[stocknum, sscol_exit_orderprice] = 0
        strategy_state.iloc[stocknum, sscol_exit_orderid] = 0
        strategy_state.iloc[stocknum, sscol_exit_orderprice] = 0
        strategy_state.iloc[stocknum, sscol_exit_filledqty] = 0
        strategy_state.iloc[stocknum, sscol_exit_balanceqty] = 0
        strategy_state.iloc[stocknum, sscol_exit_price] = 0
        strategy_state.iloc[stocknum, sscol_exit_executing] = 0
        strategy_state.iloc[stocknum, sscol_exit_reason] = 0
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None







