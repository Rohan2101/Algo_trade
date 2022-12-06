
import myutils

def GetTradePara(TradeParaFile):
    try:
        data = myutils.read_csv_to_list(TradeParaFile)
        
        if (data == None):
            return None, None, None, None, None, None, None
        
        data  = data[0]
        
        capital_allocated = data[0]
        max_capital_to_deploy = data[1]
        buy_margin = data[2]
        sell_margin = data[3]
        target = data[4]
        stoploss = data[5]
        trading_cost = data[6]

        return float(capital_allocated), float(max_capital_to_deploy), float(buy_margin), float(sell_margin), float(target), float(stoploss), float(trading_cost) 
    
    except:
        print("error")
        return None, None, None, None, None, None, None
    
def GetTradeAccountPara(TradeAccountParaFile):
    try:
        data = myutils.read_csv_to_list(TradeAccountParaFile)
        
        if (data == None):
            return None, None, None
        
        data  = data[0]
        
        userid = data[0]
        password = data[1]
        acountid = data[2]
        
        return userid, password, acountid 
    
    except:
        print("error")
        return None, None, None
    
def GetSignalPara_RSI(SignalParaFile):
    try:
        data = myutils.read_csv_to_list(SignalParaFile)
        
        if (data == None):
            return None, None, None
        
        data  = data[0]
        
        period = data[0]
        long_entry = data[1]
        short_entry = data[2]

        return int(period), int(long_entry), int(short_entry) 
    
    except:
        print("error")
        return None, None, None

    
def GetSignalPara_MACD(SignalParaFile):
    try:
        data = myutils.read_csv_to_list(SignalParaFile)
        
        if (data == None):
            return None, None, None, None
        
        data  = data[0]
        
        short_period = data[0]
        long_period = data[1]
        long_entry = data[2]
        short_entry = data[3]
        
        return int(short_period), int(long_period), int(long_entry), int(short_entry) 
        
    except:
        print("error")
        return None, None, None, None
    
def GetSignalPara_MACDHistogram(SignalParaFile):
    try:
        data = myutils.read_csv_to_list(SignalParaFile)
        
        if (data == None):
            return None, None, None, None, None
        
        data  = data[0]
        
        short_period = data[0]
        long_period = data[1]
        signal_period = data[2]
        long_entry = data[3]
        short_entry = data[4]
        
        return int(short_period), int(long_period), int(signal_period), int(long_entry), int(short_entry) 
        
    except:
        print("error")
        return None, None, None, None, None
