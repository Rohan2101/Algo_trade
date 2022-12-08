import WazirxAPI
import RSI1
import MACD_OLD
import BB_UTILS

def main_menu():
    x = 0
    print("Welcome to Cypher AI Trading Bot ")
    print("Press 1 for Generating Signals for your selected crypto ")
    print("Press 2 for Logging in to Wazirx")
    print("Press 3 for Placing order")
    print("Press 4 for Updating the historical price for your selected crypto")
    print("Press 5 to Get Current Price")
    print("Press 6 for Running Algo Trade Software and Generate Periodical Signals every Specified Amount of Time")
    x = int(input("Press 7 for Updating Historical data periodically for the Specified Amount of Time\n"))
    if x == 1:
        signals_menu()
    elif x == 2:
        WazirxAPI.login()
        main_menu()
    elif x == 3:
        WazirxAPI.login()
        print("Please input the necessary information in the following order")
        ticker = input("Input Ticker\n")
        limit = input("Input \'market\' or \'limit\'\n")
        buy = input("Input \'buy\' or \'sell\' order\n")
        amount = input("Input the amount\n")
        price = input("Input the buy or sell price\n")
        WazirxAPI.Place_order(ticker, limit, buy, amount, price)
        main_menu()
    elif x == 4:
        get_symbol_data()
        main_menu()
    elif x == 5:
        ticker = input("Input the ticker\n")
        print(WazirxAPI.get_current_price(ticker))
        main_menu()
    elif x ==6:
        print("Please input the necessary information in the following order")
        symbol = input("Please input symbol of crypto\n")
        scan_interval = int(input("Please enter the length of the time interval in minutes\n"))
        WazirxAPI.generate_hourly_signals(symbol,scan_interval)
    elif x == 7:
        print("Please input the necessary information in the following order")
        symbol = input("Please input symbol of crypto\n")
        scan_interval = int(input("Please enter the length of the time interval in minutes\n"))
        WazirxAPI.get_hourly_data(symbol, symbol, scan_interval)
    return None

def get_symbol_data():
    val = ''
    val = input("Please Press 1 for Crypto or Press 2 for Indian Stocks or write return to return to main menu\n")
    if val.lower() == "return":
        main_menu()
    elif int(val) == 1:
        symbol = input("Please input symbol\n")
        WazirxAPI.write_hist_data(symbol, symbol)
        g = WazirxAPI.read_data(symbol)
        return g
    elif int(val) == 2:
        symbol = input("Please input symbol\n")
        WazirxAPI.write_hist_data_stocks(symbol, symbol)
        g = WazirxAPI.read_data(symbol)
        return g
    else:
        print("Invalid input")
        get_symbol_data()

def signals_menu():
    x = 0
    y = 0
    if y == 0:
        y = get_symbol_data()
    #symbol = input("Enter crypto symbol\n")
    #WazirxAPI.write_hist_data(symbol, symbol)
    #y = get_symbol_data()
    print("Press 0 for returning to the main menu")
    print("Press 1 for generating RSI signal for last traded price and time")
    print("Press 2 for generating RSI signals for specified time period")
    print("Press 3 for generating MACD signals for entire time period")
    print("Press 4 for generating MACD signal of last traded price and time")
    print("Press 5 for generating BB signals for entire time period")
    print("Press 6 for generating BB signal of last traded price and time")
    print("Press 7 for generating Stochastic signals for entire time period")
    print("Press 8 for generating Stochastic signal of last traded price and time")
    x = int(input("Press 9 for generating combined signal for the last traded price and time\n"))
    if x == 0:
        main_menu()
    elif x == 1:
        period = int(input("Please input the period for which the RSI needs to be calculated\n"))
        print(WazirxAPI.Get_all_RSI_signals(y, period))
        signals_menu()
    elif x == 2:
        f = int(input("Press 1 for RSI values, Press 2 for RSI signals or Press 3 for RSI plot\n"))
        if f == 1:
            period = 0
            period = int(input("Please input the period for which the RSI needs to be calculated\n"))
            j1 = RSI1.get_rsi(y,period)
            print(j1[-30:-1])
        elif f == 2:
            period = 0
            period = int(input("Please input the period for which the RSI needs to be calculated\n"))
            y2 = RSI1.get_rsi(y, period)
            j2 = RSI1.get_rsi_signal(y2)
            print(j2[-30:-1])
        elif f == 3:
            period = 0
            period = int(input("Please input the period for which the RSI needs to be calculated\n"))
            y2 = RSI1.get_rsi(y, period)
            y3 = RSI1.get_rsi_signal(y2)
            RSI1.plot_rsi_buy_sell(y2,y3)
        #print(WazirxAPI.Get_RSI_signals(y))
        signals_menu()
    elif x == 3:
        f = 0
        f = int(input("Press 1 for MACD signals or Press 2 for MACD plot\n"))
        if f == 1:
            print(WazirxAPI.get_MACD_signalline(y))
        elif f == 2:
            f1 = 0
            f1 = int(input("Press 1 for MACD signals plot or Press 2 for MACD Crossover signals plot\n"))
            y3 = MACD_OLD.get_macd_signal_line(y)
            if f1 == 1:
                y5 = MACD_OLD.get_signal_macd_signalline(y3)
                print(y5[-30:-1])
                MACD_OLD.plot_macd_buy_sell(y3,y5)
            elif f1 == 2:
                y4 = MACD_OLD.get_signal_macd_crossover(y3)
                print(y4[-30:-1])
                MACD_OLD.plot_macd_buy_sell(y3,y4)
        signals_menu()
    elif x ==4 :
        print(WazirxAPI.get_MACD_signal(y))
        signals_menu()
    elif x == 5:
        f3 = 0
        f3 = int(input("Please 1 for bb signals or Press 2 for bb_plot of the signals for entire time period\n"))
        if f3 == 1:
            print(WazirxAPI.get_bb_signals(y))
        elif f3 == 2:
            g1 = BB_UTILS.get_bb_values(y)
            g2 = BB_UTILS.get_bb_signal(g1)
            BB_UTILS.plot_bb_buy_sell(g1,g2)
        signals_menu()
    elif x == 6:
        print(WazirxAPI.get_bb_signal(y))
        signals_menu()
    elif x == 7:
        print(WazirxAPI.get_Stochastic_signals(y))
        signals_menu()
    elif x ==8 :
        print(WazirxAPI.get_Stochastic_signal(y))
        signals_menu()
    elif x == 9:
        print(WazirxAPI.get_combined_signal(y))
        signals_menu()
    else:
        print("Wrong input, Please input a valid response")
        signals_menu()

    return None
main_menu()