import pandas as pd

import signal_generators
import JupitronAPI
import myutils
import yfinance as yf
import trade_generator
import re

#print(generate_signal_RSI('nse_fo_master', 49500, 70, 10, 9, ''))
#print(JupitronAPI.)
z = pd.read_csv('RSIStrategyState.csv')
w = []
for i in z['TrdSymbol']:
    r = re.sub('22OCTFUT', '',i)
    w.append(r)
    data2 = yf.download(tickers= r + '.NS', period='90d', interval='60m')
    myutils.write_dataframe(r,data2)
#data2 = yf.download(tickers='ADANIPORTS.NS', period= '90d', interval= '60m')
#myutils.write_dataframe('ADANIPORTS',data2)
#trade_generator.generate_trade(68.33776092529297, -1, 100, -1, .75, 1000, 5, 5, 100, 5, 50, 100, 'previous_exit_reason')