# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 10:45:01 2022

@author: User1
"""

import indicators
import myutils
import sys


def generate_signal_RSI(symbol_name, ltp, period, long_entry, short_entry, data_path ):
    try:
        
        symbol_name = symbol_name.strip()
        
        if type(ltp) is str:
            ltp = float(ltp.strip())
        
        if type(period) is str:
            period = int(period.strip())
        
        if type(long_entry) is str:
            long_entry = float(long_entry.strip())
        
        if type(short_entry) is str:
            short_entry = float(short_entry.strip())
        
        if (symbol_name == '' or ltp <= 0 or period <= 2 or long_entry <= 0 or long_entry > 100 or short_entry <= 0 or short_entry > 100 or long_entry <= short_entry ):
            print(sys._getframe().f_code.co_name,'Invalid parameter values')
            return None
        
        data = myutils.read_dataframe(data_path + '' + symbol_name + '.csv')

        
        if (data.empty):
            print(sys._getframe().f_code.co_name,'Data not found')
            return None
        
        # specific to your data set, modify accordingly
        data = data['Close']
        
        data = data.dropna()
        
        #data = data[-period:]
        
        current_rsi = indicators.RSI(data, period)
        
        if (current_rsi == None):
            return None
        
        print('RSI ' + str(current_rsi))
        
        if (current_rsi > long_entry):
            signal = 1
        elif (current_rsi < short_entry):
            signal = -1
        else:
            signal = 0
            
        return signal
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None
#print(generate_signal_RSI('ADANIPORTS', 49500, 14, 70, 30, ''))
#p = open('/nse_fo_master.csv', 'r')
#print(p)
def generate_signal_MACD(symbol_name, ltp, short_window, long_window, long_entry, short_entry, data_path ):
    try:
        
        symbol_name = symbol_name.strip()
        
        if type(ltp) is str:
            ltp = float(ltp.strip())
        
        if type(short_window) is str:
            short_window = int(short_window.strip())
       
        if type(long_window) is str:
            long_window = int(long_window.strip())
        
        if type(long_entry) is str:
            long_entry = float(long_entry.strip())
        
        if type(short_entry) is str:
            short_entry = float(short_entry.strip())
        
        if (symbol_name == '' or ltp <= 0 or short_window < 1 or long_window <= short_window or long_entry < 1 or short_entry <= 0 or short_entry > 1):
            print(sys._getframe().f_code.co_name,'Invalid parameter values')
            return None
        
        data = myutils.read_dataframe(data_path + '' + symbol_name + '.csv')
        
        if (data.empty):
            print(sys._getframe().f_code.co_name,'Data not found')
            return None
        
        # specific to your data set, modify accordingly
        data = data['Close']
        
        data = data.dropna()
        
        #data = data[-period:]
        
        current_macd = indicators.MACD(data, short_window, long_window)


        if (current_macd == None):
            return None
        
        print('MACD ' + str(current_macd))
        
        data['Long_MA'] = data[-long_window:].ewm(span = long_window, adjust = False).mean()
        
        LMA = data['Long_MA'].iloc[-1]
        print(current_macd,LMA)
        print(LMA * long_entry)
        print(-LMA * short_entry)
        if (current_macd > LMA * long_entry):
            signal = 1
        elif (current_macd < -LMA * short_entry):
            signal = -1
        else:
            signal = 0
        
        return signal
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None
            
#print(generate_signal_MACD('matic', 68.33776092529297,20,50,2,.5,''))

def generate_signal_MACD_Histogram(symbol_name, ltp, short_window, long_window, signal_window, long_entry, short_entry, data_path ):
    try:
        
        symbol_name = symbol_name.strip()
        
        if type(ltp) == str:
            ltp = float(ltp.strip())
        
        if type(short_window) is str:
            short_window = int(short_window.strip())
       
        if type(long_window) is str:
            long_window = int(long_window.strip())
       
        if type(signal_window) is str:
            signal_window = int(signal_window.strip())
        
        if type(long_entry) is str:
            long_entry = float(long_entry.strip())
        
        if type(short_entry) is str:
            short_entry = float(short_entry.strip())
        
        if (symbol_name == '' or ltp <= 0 or short_window < 1 or long_window <= short_window or signal_window < 1 or long_entry < 1 or short_entry <= 0 or short_entry > 1):
            print(sys._getframe().f_code.co_name,'Invalid parameter values')
            return None
        
        data = myutils.read_dataframe(data_path + '' + symbol_name + '.csv')
        
        if (data.empty):
            print(sys._getframe().f_code.co_name,'Data not found')
            return None
        
        # specific to your data set, modify accordingly
        data = data['Close']
        
        data = data.dropna()
        
        #data = data[-period:]
        
        current_macd_histogram = indicators.MACD_Histogram(data, short_window, long_window, signal_window)
        
        if (current_macd_histogram == None):
            return None
        
        print('MACD Histogram ' + str(current_macd_histogram))
        
#        data['Long_MA'] = data['Close'][-long_window:].ewm(span = long_window, adjust = False).mean()
        
#        LMA = data['Long_MA'][-1]
        
        if (current_macd_histogram > 0):
            signal = 1
        elif (current_macd_histogram < 0):
            signal = -1
        else:
            signal = 0
        
        return signal
        
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None
            
print(generate_signal_MACD_Histogram('matic',68.33776092529297, 20,50, 14,2,.75,''))
