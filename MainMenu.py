import WazirxAPI


def main_menu():
    x = 0
    print("Welcome to Cypher AI Trading Bot ")
    print("Press 1 for generating signals for your selected crypto ")
    print("Press 2 for logging in to wazir x")
    print("Press 3 for Placing order")
    print("Press 4 for updating the historical price for your selected crypto")
    print("Press 5 to get current Price")
    print("Press 6 for running algo trade software and generate periodical signals every specified amount of time")
    x = int(input("Press 7 for updating hist data periodically for the specified amount of time\n"))
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
    symbol = input("Please input symbol of crypto or write return to return to main menu\n")
    if symbol.lower() == "return":
        main_menu()
    WazirxAPI.write_hist_data(symbol, symbol)
    g = WazirxAPI.read_data(symbol)
    return g


def signals_menu():
    x = 0
    y =0
    if y == 0:
        y = get_symbol_data()
    #symbol = input("Enter crypto symbol\n")
    #WazirxAPI.write_hist_data(symbol, symbol)
    #y = get_symbol_data()
    print("Press 0 for returning to the main menu")
    print("Press 1 for generating RSI signals for entire time period")
    print("Press 2 for generating RSI signal of last traded price and time")
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
        print(WazirxAPI.Get_all_RSI_signals(y))
        signals_menu()
    elif x == 2:
        print(WazirxAPI.Get_RSI_signals(y))
        signals_menu()
    elif x == 3:
        print(WazirxAPI.get_MACD_signalline(y))
        signals_menu()
    elif x ==4 :
        print(WazirxAPI.get_MACD_signal(y))
        signals_menu()
    elif x == 5:
        print(WazirxAPI.get_bb_signals(y))
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