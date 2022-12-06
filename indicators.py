# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 10:27:46 2022

@author: User1
"""

import pandas as pd
import numpy as np
import sys


def RSI(data, period):
    try:
        
        if (len(data) < period):
            print(sys._getframe().f_code.co_name,'Insufficient data')
            return None
        
        if (period < 1):
            print(sys._getframe().f_code.co_name,'Invalid parameter value for period')
            return None
        
        data = pd.DataFrame(data[-period:])
        
        data['change'] = data['Close'].diff()
        
        data['gain'] = data['change']
        data.loc[data['gain'] < 0, ['gain']] = 0.0
        
        data['loss'] = data['change']
        data.loc[data['loss'] > 0, ['loss']] = 0.0
        data['loss'] = abs(data['loss'])
        
        avg_gain = data['gain'].mean()
        avg_loss = data['loss'].mean()
        
        RS = avg_gain / avg_loss
        
        RSI = 100.0 - (100.0 / ( 1.0 + RS ))
        print(data)
        #print(avg_gain, avg_loss)
        #print(RSI)
        return RSI
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None
    

def MACD(data, short_window, long_window):
    try:
        
        if (len(data) < long_window):
            print(sys._getframe().f_code.co_name,'Insufficient data')
            return None
        
        if (short_window < 1):
            print(sys._getframe().f_code.co_name,'Invalid parameter value for short_window')
            return None
        
        if (long_window <= short_window):
            print(sys._getframe().f_code.co_name,'Invalid parameter value for long_window')
            return None
        
        data = pd.DataFrame(data[-long_window:])

#        data['Short_MA'] = data['Close'].rolling(window = short_window, center = False).mean()
        data['Short_MA'] = data['Close'].ewm(span = short_window, adjust = False).mean()
        
#        data['Long_MA'] = data['Close'].rolling(window = long_window, center = False).mean()
        data['Long_MA'] = data['Close'].ewm(span = long_window, adjust = False).mean()
        
        data['MACD'] = data['Short_MA'] - data['Long_MA']
        
        MACD = float(data['MACD'].iloc[-1])
        
        return MACD
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None


def MACD_Histogram(data, short_window, long_window, signal_window):
    try:
        
        if (len(data) < (long_window + signal_window - 1)):
            print(sys._getframe().f_code.co_name,'Insufficient data')
            return None
        
        if (short_window < 1):
            print(sys._getframe().f_code.co_name,'Invalid parameter value for short_window')
            return None
        
        if (long_window <= short_window):
            print(sys._getframe().f_code.co_name,'Invalid parameter value for long_window')
            return None
        
        if (signal_window < 1):
            print(sys._getframe().f_code.co_name,'Invalid parameter value for signal_window')
            return None
        
        data = pd.DataFrame(data[-(long_window + signal_window -1):])
        
        data['Short_MA'] = data['Close'].ewm(span = short_window, adjust = False).mean()
        
        data['Long_MA'] = data['Close'].ewm(span = long_window, adjust = False).mean()
        
        data['MACD'] = data['Short_MA'] - data['Long_MA']
        
        data['MACD_Signal'] = data['MACD'].ewm(span = signal_window, adjust = False).mean()
        
        data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
        
        #MACD_Histogram = float(data['MACD_Histogram'].iloc[-1])
        signals = data
        signals['buy_sell'] = 0.0
        signals['buy_sell'][long_window:] = np.where((data.MACD)[long_window:] > 0, 1.0, 0.0)
        signals['buy_sell'] = signals['buy_sell'].diff()
        
        return signals
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None
    
    
    