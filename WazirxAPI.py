import ccxt
import time
import yfinance as yf
import myutils
import indicators
import numpy as np
import pandas as pd

exchange_id = 'wazirx'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': 'sbMNY7Udn3iwi6YrmOMcbfJDWd94hlSHB0HkY9zPMVBkeKDVtqF6sXLlodszAHJc',
    'secret': 'O6gm86QkqnN61rxduqhR7pgHBSIZnaZtGxBTImx1',
})
def login():
# from variable id
    try:
        exchange_id = 'wazirx'
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'apiKey': 'sbMNY7Udn3iwi6YrmOMcbfJDWd94hlSHB0HkY9zPMVBkeKDVtqF6sXLlodszAHJc',
            'secret': 'O6gm86QkqnN61rxduqhR7pgHBSIZnaZtGxBTImx1',
            })
        if exchange==None:
            print("Error with connection")
        else:
            return print('Login successful')

    except:
        exchange = None

def Place_order(ticker,limit, buy, amount, price):
    markets = exchange.createOrder(str(ticker), str(limit), str(buy), int(amount), int(price))
    print(markets)
    if markets == None:
        print("Error with connection")
    else:
        return print('Order placed successfully')

def get_current_prices_dir(ticker):
    a = exchange.fetchTicker(str(ticker))
    if a == None:
        print("Error with connection")
    else:
        return a

def get_current_price(ticker):
    a = exchange.fetchTicker(str(ticker))
    if a == None:
        print("Error with connection")
    else:
        return a['ask']

def write_hist_data(symbol, file_name):
    data2 = yf.download(str(symbol) + '-INR', period= '90d', interval= '60m')
    myutils.write_dataframe(file_name, data2)
    #if data2 == None:
    #    print('Error while adding hist data')
    #else:
    return print('Hist data has been written to main file')

def write_hist_data_stocks(symbol, file_name):
    data2 = yf.download(str(symbol) + '.NS', period= '90d', interval= '60m')
    myutils.write_dataframe(file_name, data2)
    #if data2 == None:
    #    print('Error while adding hist data')
    #else:
    return print('Hist data has been written to main file')

def read_data(filename):
    filename1 = filename +'.csv'
    data = myutils.read_dataframe(filename1)
    return data


def Get_RSI_signals(data, llimit=20, hlimit=80, period=14):
    RSI = indicators.RSI(data,period)
    if RSI > hlimit:
        signal = -1
    elif RSI < llimit:
        signal = 1
    else:
        signal = 0
    return RSI

def Get_all_RSI_signals(data, llimit=20, hlimit=80, period=14):
    RSI = indicators.RSI(data,period)
    if RSI > hlimit:
        signal = -1
    elif RSI < llimit:
        signal = 1
    else:
        signal = 0
    return signal


def Get_MACD_signals(data, short_window = 20, long_window = 50):
    MACD = indicators.MACD(data, short_window, long_window)
    return MACD

def get_MACD_signalline(data, short_window = 20, long_window = 50, signal_window=12):
    macd_data = data.copy()
    # Create the set of short and long simple moving average, MACD, signal line over the
    # respective periods
    macd_data["SMA"] = macd_data['Close'].rolling(window = short_window, center=False).mean()
    macd_data["LMA"] = macd_data['Close'].rolling(window = long_window, center=False).mean()
    macd_data["MACD"] = macd_data['SMA'] - macd_data['LMA']
    macd_data['signal_line'] = macd_data['MACD'].rolling(window = signal_window).mean()

    #signals = pd.DataFrame(index = macd_data.index)
    signals= macd_data.copy()
    signals['buy_sell'] = 0.0
    signals['buy_sell'][long_window:] = np.where((macd_data.MACD)[long_window:]
                                            > 0, 1.0, 0.0)
    signals['buy_sell'] = signals['buy_sell'].diff()
    # return buy and sell signal
    signals1 = pd.DataFrame(index=signals.index)
    signals1 = signals
    signals1['buy_sell'] = 0.0
    signals1['buy_sell'][long_window:] = np.where((signals.MACD)[long_window:]
                                            > signals.signal_line[long_window:], 1.0, 0.0)
    signals1['buy_sell'] = signals1['buy_sell'].diff()
    return signals1

def plot_macd_buy_sell(macd_signal_line, signals, symbol):
    """
    Plot for macd price, shortma, longma, buy signal, sell signal
    Input: data frame with all above information
    Output: None
    """
    # putting all above together
    fig = plt.figure(figsize=(15, 15))
    plt.title(symbol)
    # fig1
    ax1 = fig.add_subplot(411, ylabel='Price in $')
    macd_signal_line['price'].plot(ax=ax1, color='r', lw=2.)
    macd_signal_line[['SMA', 'LMA']].plot(ax=ax1, lw=2.)
    # fig2
    ax2 = fig.add_subplot(412, ylabel='buy signal')
    signals['price'].plot(ax=ax2, color='r', lw=2.)
    ax2.plot(signals.loc[signals.buy_sell == 1.0].index, signals.price[signals.buy_sell == 1.0], '^', markersize=10,
             color='m')
    # fig3
    ax3 = fig.add_subplot(413, ylabel='sell signal')
    signals['price'].plot(ax=ax3, color='r', lw=2.)
    ax3.plot(signals.loc[signals.buy_sell == -1.0].index, signals.price[signals.buy_sell == -1.0], 'v', markersize=10,
             color='k')
    # fig4
    ax4 = fig.add_subplot(414, ylabel='buy sell signal')
    signals['price'].plot(ax=ax4, color='r', lw=2.)
    # add buy sell
    ax4.plot(signals.loc[signals.buy_sell == 1.0].index, signals.price[signals.buy_sell == 1.0], '^', markersize=10,
             color='g')
    ax4.plot(signals.loc[signals.buy_sell == -1.0].index, signals.price[signals.buy_sell == -1.0], 'v', markersize=10,
             color='k')
    #
    plt.show()

def get_MACD_signal(data):
    data1 = get_MACD_signalline(data)
    return data1['buy_sell'].iloc[-1]

def get_combined_signal(data):
    x = Get_all_RSI_signals(data)
    y1 = get_MACD_signalline(data)
    y = get_MACD_signal(y1)
    z = get_bb_signal(data)
    xy = 0
    if (x == 1 and y == 1) or (y == 1 and z == 1) or (x == 1 and z == 1):
        xy = 1
    elif (x == -1 and y == -1) or (y == -1 and z == -1) or (x == -1 and z == -1):
        xy = -1
    else:
        pass
    return xy, x, y, z

def get_bb_signals(data, period = 20, std = 2):
    bb_data = pd.DataFrame(index=data.index)
    bb_data['price'] = data['Close']
    bb_data['Datetime'] = data['Datetime']
    bb_data['middleband'] = bb_data['price'].rolling(window=period).mean()
    bb_data['upperband'] = bb_data['middleband'] + std * (bb_data['price'].rolling(window=period).std())
    bb_data['lowerband'] = bb_data['middleband'] - std * (bb_data['price'].rolling(window=period).std())
    signals = pd.DataFrame(index=bb_data.index)
    signals.head()
    signals['Datetime'] = bb_data['Datetime']
    signals['price'] = bb_data['price']
    signals['sell']= 0.0
    signals['buy']= 0.0
    signals['buy'][period:] = np.where(bb_data['price'][period:] < bb_data['lowerband'][period:], -1.0, 0.0)
    signals['sell'][period:] = np.where(bb_data['price'][period:] > bb_data['upperband'][period:],1.0,0)
    signals['buy'] = signals['buy'].diff()
    signals['sell'] = signals['sell'].diff()
    signals.loc[signals['buy'] == -1.0,['buy']]=0
    signals.loc[signals['sell'] == 1.0,['sell']]=0
    signals['buy_sell'] = signals['buy'] + signals['sell']

    return signals[['Datetime','price', 'buy_sell']]

def get_bb_signal(data, period = 20, std = 2):
    x = get_bb_signals(data, period, std)
    return x['buy_sell'].iloc[-1]

def plot_bb_buy_sell(bb, signals):
    """
    Plot price, Bollinger band middle, lower, upper band with buy and sell signal
    """
    graph = plt.figure(figsize=(20,5))
    ax1 = graph.add_subplot(111)
    bb[['price','lowerband','upperband']].plot(ax = ax1,title ='Bollinger band Signals')
    ax1.plot(signals.loc[signals.buy_sell == 1].index, signals.price[signals.buy_sell == 1], "^", markersize = 12, color = "g")
    ax1.plot(signals.loc[signals.buy_sell == -1].index, signals.price[signals.buy_sell == -1], "v", markersize = 12, color = "m")
    # plt.show()
    plt.show()

def get_Stochastic_signals(data, level=7):
    data['H-14'] = data['High'].shift(14)
    data['L-14'] = data['Low'].shift(14)
    data['Stochastic value'] = (data['Close'] - data['L-14']) / (data['H-14'] - data['L-14'])
    data['Slow Stochastic'] = data['Stochastic value'].rolling(3).mean()
    data['price'] = data['Close'].copy()
    data['S-Sigmoid'] = 1 / (1 + data['Slow Stochastic']) * 100
    data.loc[data['Slow Stochastic'] > level, ['sell_signal']] = -1
    data.loc[data['Slow Stochastic'] < level, ['sell_signal']] = 0.0
    data.loc[data['Slow Stochastic'] < -level, ['buy_signal']] = 1
    data.loc[data['Slow Stochastic'] > -level, ['buy_signal']] = 0
    print(data.iloc[-20:-1])
    return data

def get_Stochastic_signal(data, level=7):
    data['H-14'] = data['High'].shift(14)
    data['L-14'] = data['Low'].shift(14)
    data['Stochastic value'] = (data['Close'] - data['L-14']) / (data['H-14'] - data['L-14'])
    data['Slow Stochastic'] = data['Stochastic value'].rolling(3).mean()
    data['price'] = data['Close'].copy()
    data['S-Sigmoid'] = 1 / (1 + data['Slow Stochastic']) * 100
    data.loc[data['Slow Stochastic'] > level, ['sell_signal']] = -1
    data.loc[data['Slow Stochastic'] < level, ['sell_signal']] = 0.0
    data.loc[data['Slow Stochastic'] < -level, ['buy_signal']] = 1
    data.loc[data['Slow Stochastic'] > -level, ['buy_signal']] = 0
    return data.iloc[-1]['buy_signal'], data.iloc[-1]['sell_signal']

def get_hourly_data(symbol, file_name, scan_interval=10):
    x = 0
    while x == 0:
        write_hist_data(symbol, file_name)
        print(f'Scan complete, waiting for {scan_interval} mins for next Check')
        time.sleep(scan_interval * 60)
    return print("Scanned and saved")

def generate_hourly_signals(symbol, scan_interval=10):
    x= 0
    while x == 0:
        write_hist_data(symbol, symbol)
        data = read_data(symbol)
        print(get_combined_signal(data))
        print(f'Scan complete, waiting for {scan_interval} mins for next Check')
        time.sleep(scan_interval * 60)
    return print("Scanned")



#data = get_current_price('FTM/INR')
#print(data)
#write_hist_data('MATIC', 'MATIC')
#y = read_data('FTM')
#print(Get_all_RSI_signals(y))
#print(Get_MACD_signals(y))
#x = get_MACD_signalline(y, )
#print(x[x['buy_sell'] == 1])
#print(get_MACD_signalline(y))
#print(x['buy_sell'].iloc[-1])
#print(get_MACD_signal(x))
#print(get_combined_signal(y))
#print(get_bb_signals(y))
#print(get_bb_signal(y))
#print(get_Stochastic_signals(y, 10))
#get_hourly_data('FTM', 'FTM', 2)
#print(generate_hourly_signals('FTM', 'FTM',y,2))
