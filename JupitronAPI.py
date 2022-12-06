# -*- coding: utf-8 -*-
"""
Created on Mon Nov 3 20:42:57 2020

@author: Abhijit Biswas
@Copyright: Quant Qubit Pvt. Ltd. All Right Reserved.
"""

import socket
import csv
import pandas as pd
import requests


class Jupitron:
    """
    A class to access the Jupitron API functions


    Attributes
    ----------
    APIHost : string
        A string to specify the IP address of the machine where the Jupitron Server is running. 

    APIPort : integer
        An integer to specify the Port on which the Jupitron Server is running

    APIKey : string
        A string to specify the Authentication Key for communication with the Jupitron Server 
        
    Methods
    -------
    GetQuote(Exchange, Symbol)
        Function to get the live market price quotes for the specified symbol.
        Returns a dictionary object with the LTP, BidPrice, AskPrice, LTQ, BidQty, AskQty, Open, High, Low, Close, Trade Volume, Average Price
        
    GetIndiaVIX()
        Function to get the live market India VIX index.
        Returns a dictionary object with the LTP
        
    GetOHLC(Exchange, Symbol)
        Function to get the live market OHLC price quotes for the specified symbol.
        Returns a dictionary object with the LTP, Open, High, Low, Close
    
    GetOrderBookQuote(Exchange, Symbol)
        Function to get the live market Order Book quotes for the specified symbol.
        Returns a dictionary object with the top 5 levels depth quotes for 
        BidPrice, AskPrice, BidQty, AskQty, BidOrders, AskOrders
    
    PlaceOrder(Exchange, TrdSymbol, OrderQty, OrderPrice, BuyOrSell, AccountId, OrderValidity, OrderPriceType, OrderProductType, OrderByCustFirm)
        Function to place orders.
        Returns the GUIOrderID if Jupitron Server could place the order, else returns nothing
    
    ModifyOrder(Exchange, GUIOrderID, OrderQty, OrderPrice, OrderValidity, OrderPriceType)
        Function to modify orders.
        Returns a number specifying the result of the operation
    
    CancelOrder(GUIOrderID)
        Function to modify orders.
        Returns a number specifying the result of the operation
    
    GetOrderStatus(GUIOrderID)
        Function to get the status of a placed order.
        Returns a dictionary object with 
        GUIOrdID, NestOrdNum, ExchOrdId, QuanToFill, FilledShares, UnfilledSize, CancelledSize, Price, AvgPrice, 
        NestUpdateTime, ExchTime, ExchOrdUpdateTime, Status, OrdStatus, RejReason
        
    GetOrderHistory()
        Function to get the details of all the placed order.
        Returns a Pandas DataFrame with the columns
        GuiOrdId, NestOrdNum, ExchOrdId, ExchSeg, TrdSymbol, Symbol, Price, Quantity, TransType, AvgPrice, 
        FilledShares, UnfilledSize, Status, RejReason, ExchTime, FillTime, Product, AccountId
    
    GetTradeHistory()
        Function to get the details of all the trades.
        Returns a Pandas DataFrame with the columns 
        GuiOrdId, NestOrdNum, ExchOrdId, ExchSeg, TrdSymbol, Symbol, FillPrice, FillSize, TransType, FillLeg, 
        FillStatus, Status, ExchTime, FillTime, Product, AccountId
    
    GetErrorMessages()
        Function to get all the error messages from the Jupitron Server.
        Returns a list of all the error messages since the last read.
    
    GetMasterData()
        Function to get the master data of instruments for an exchange.
        Returns a list of master data of instruments.
        
    """
    

    #############################################################################################################
    #   Private Functions
    #############################################################################################################
    
    def __GetDataFromJupitron(self, request, isresponsebig = False):
        try:
            request = self.ip + '\n' + self.sessiontoken + '\n' + self.api_key + '\n' + request
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
                sck.connect((self.host, self.port))
                sck.sendall(bytes(request, 'utf-8'))
                
                if (isresponsebig):
                    response = ''
                    data = sck.recv(65535)
                    while len(data) > 0:
                        response = response + data.decode('utf-8')
                        data = sck.recv(65535)
                    sck.close()
                else:
                    response = sck.recv(65535)
                    sck.close()
                    response = response.decode('utf-8')
        except OSError:
            raise OSError
        except:
            response = None
        
        return response
    
    def __GetAPIHost(self):
        try:
            myfile = open('JupitronAPIHost.txt')
            with myfile:
                reader = csv.reader(myfile)
                for row in reader:
                    host = row[0]
                    break
            myfile.close()
        except:
            host = ''
        
        return host
    
    def __GetAPIPort(self):
        try:
            myfile = open('JupitronAPIPort.txt')
            with myfile:
                reader = csv.reader(myfile)
                for row in reader:
                    apiport = row[0]
                    break
            myfile.close()
        except:
            apiport = '45000'
        
        return int(apiport)

    def __GetAPIKey(self):
        try:
            myfile = open('JupitronAPIKey.txt')
            with myfile:
                reader = csv.reader(myfile)
                for row in reader:
                    apikey = row[0]
                    break
            myfile.close()
        except:
            apikey = ''
        
        return apikey
    
    def __init__(self):
        """
        Parameters
        ----------
        APIHost : string
            A string to specify the IP address of the machine where the Jupitron Server is running. 
    
        APIPort : integer
            An integer to specify the Port on which the Jupitron Server is running
    
        APIKey : string
            A string to specify the Authentication Key for communication with the Jupitron Server 
        """
        
        try:
            self.host = self.__GetAPIHost()
            self.port = self.__GetAPIPort()
            self.api_key = self.__GetAPIKey()
            self.ip = requests.get('https://api.ipify.org').text
            self.sessiontoken = ''
        except:
            print('Error')
        
 
    
    
       
    #############################################################################################################
    #   Public Functions
    #############################################################################################################
        
    def Login(self, Username, Password):
        """
        Function to login to JupiTron server. Returns a session token.
        
        Parameters
        ----------
        Username : string
            The username
        
        Password : string
            The password
                
        APIKey : string
            The APIKey

        Returns
        ----------
        SessionToken : string
            A session token if login is successful.
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            self.sessiontoken = ''
            if (Username.strip() == '' or Password == ''):
                return {'Input Error' : 'One or more mandatory parameters not specified properly'}
            request = 'LOGIN' + '\n' + Username + '\n' + Password
            response = self.__GetDataFromJupitron(request)
            if (response == None or response == ''):
                return None
            response = response.split('\n')
            if (response[0] == '1'):
                response = {'Message' : 'Login Failed. Invalid login details.'}
            elif (response[0] == '2'):
                response = {'Message' : 'Login Failed. Wrong username or password.'}
            elif (response[0] != '6'):
                response = {'Message' : 'Login Failed. Invalid login details.'}
            else:
                self.sessiontoken = response[1]
                response = {'Message' : 'Login Successful'}
        except:
            response = None
        
        return response
    #############################################################################################################
    
    def GetQuote(self, Exchange, Symbol):
        """
        Function to get the live market price quotes for the specified symbol. Returns a dictionary object.
        
        Parameters
        ----------
        Exchange : string
            The symbol of the Exchange in lower case
        
        Symbol : string
            The symbol of the stock
        
        Returns
        ----------
        LTP : float
            The last traded price
        
        BidPrice : float
            The top Bid price quote
        
        AskPrice : float
            The top Ask price quote
        
        LTQ : integer
            The Last Traded Quantity
        
        BidQty : integer
            The top Bid quote quantity
        
        AskQty : integer
            The top Ask quote quantity
        
        Open : float
            The day Open price
        
        High : float
            The day High price
        
        Low : float
            The day Low price
        
        Close : float
            The previous day Closing price
        
        Trade Volume : integer
            The Last Traded Quantity
        
        Average Price  : float
            The average traded price of the day
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            if (Exchange.strip() == '' or Symbol.strip() == ''):
                return {'Input Error' : 'One or more mandatory parameters not specified properly'}
            request = 'GET_QUOTE1' + '\n' + Exchange + '\n' + Symbol
            print(request)
            response = self.__GetDataFromJupitron(request)
            print(response)
            if (response == None or response == '' or response == '14'):
                return None
            response = response.split('|')
            response = {'LTP' : response[0], 'BidPrice' : response[1], 'AskPrice' : response[2], 
                        'LTQ' : response[3], 'BidQty' : response[4], 'AskQty' : response[5], 
                        'Open' : response[6], 'High' : response[7], 'Low' : response[8], 'Close' : response[9], 
                        'TrdVolume' : response[10], 'AvgPrice' : response[11]}
        except:
            response = None
        
        return response
    #############################################################################################################

    
    def GetIndiaVIX(self):
        """
        Function to get the live market India VIX index. Returns a dictionary object.
        
        Parameters
        ----------
        No parameters
        
        Returns
        ----------
        LTP : float
            The last traded price
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            request = 'GET_INDEX_UPDATES'
            response = self.__GetDataFromJupitron(request)
            if (response == None or response == '' or response == '14'):
                return None
            response = response.split('|')
            response = {'LTP' : response[6]}
        except:
            response = None
        
        return response
    #############################################################################################################
    
    
    def GetOHLC(self, Exchange, Symbol):
        """
        Function to get the live market OHLC price quotes for the specified symbol. Returns a dictionary object.
        
        Parameters
        ----------
        Exchange : string
            The symbol of the Exchange in lower case
        
        Symbol : string
            The symbol of the stock
        
        Returns
        ----------
        LTP : float
            The last traded price
        
        Open : float
            The day Open price
        
        High : float
            The day High price
        
        Low : float
            The day Low price
        
        Close : float
            The previous day Closing price
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            if (Exchange.strip() == '' or Symbol.strip() == ''):
                return {'Input Error' : 'One or more mandatory parameters not specified properly'}
            request = 'GET_OHLC1' + '\n' + Exchange + '\n' + Symbol
            response = self.__GetDataFromJupitron(request)
            if (response == None or response == '' or response == '14'):
                return None
            response = response.split('|')
            response = {'LTP' : response[0], 'Open' : response[1], 'High' : response[2], 'Low' : response[3], 
                        'Close' : response[4]}
        except:
            response = None
        
        return response
    #############################################################################################################
    
    
    def GetOrderBookQuote(self, Exchange, Symbol):
        """
        Function to get the live market Order Book quotes for the specified symbol.
        Returns a dictionary object with the top 5 levels depth quotes.
        
        Parameters
        ----------
        Exchange : string
            The symbol of the Exchange in lower case
        
        Symbol : string
            The symbol of the stock
        
        Returns
        ----------
        BidPrice_1 : float
            The top Bid price quote
        
        AskPrice_1 : float
            The top Ask price quote
        
        BidQty_1 : integer
            The top Bid quote quantity
        
        AskQty_1 : integer
            The top Ask quote quantity
        
        BidOrders_1 : integer
            The top Bid quote quantity
        
        AskOrders_1 : integer
            The top Ask quote quantity
        BidPrice_2 : float
            The top Bid price quote
        
        AskPrice_2 : float
            The top Ask price quote
        
        BidQty_2 : integer
            The top Bid quote quantity
        
        AskQty_2 : integer
            The top Ask quote quantity
        
        BidOrders_2 : integer
            The top Bid quote quantity
        
        AskOrders_2 : integer
            The top Ask quote quantity
        BidPrice_3 : float
            The top Bid price quote
        
        AskPrice_3 : float
            The top Ask price quote
        
        BidQty_3 : integer
            The top Bid quote quantity
        
        AskQty_3 : integer
            The top Ask quote quantity
        
        BidOrders_3 : integer
            The top Bid quote quantity
        
        AskOrders_3 : integer
            The top Ask quote quantity
        BidPrice_4 : float
            The top Bid price quote
        
        AskPrice_4 : float
            The top Ask price quote
        
        BidQty_4 : integer
            The top Bid quote quantity
        
        AskQty_4 : integer
            The top Ask quote quantity
        
        BidOrders_4 : integer
            The top Bid quote quantity
        
        AskOrders_4 : integer
            The top Ask quote quantity
        BidPrice_5 : float
            The top Bid price quote
        
        AskPrice_5 : float
            The top Ask price quote
        
        BidQty_5 : integer
            The top Bid quote quantity
        
        AskQty_5 : integer
            The top Ask quote quantity
        
        BidOrders_5 : integer
            The top Bid quote quantity
        
        AskOrders_5 : integer
            The top Ask quote quantity
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            if (Exchange.strip() == '' or Symbol.strip() == ''):
                return {'Input Error' : 'One or more mandatory parameters not specified properly'}
            request = 'GET_ORDER_BOOK_QUOTE1' + '\n' + Exchange + '\n' + Symbol
            response = self.__GetDataFromJupitron(request)
            if (response == None or response == '' or response == '14'):
                return None
            response = response.split('\n')
            
            responsedict = {}
            for i in range(len(response)):
                fields = response[i].split('|')
                
                responsedict.update({'BidPrice_' + str(i+1) : fields[0], 'AskPrice_' + str(i+1) : fields[1], 
                                    'BidQty_' + str(i+1) : fields[2], 'AskQty_' + str(i+1) : fields[3], 
                                    'BidOrders_' + str(i+1) : fields[4], 'AskOrders_' + str(i+1) : fields[5]})
           
        except:
            responsedict = None
        
        return responsedict
    #############################################################################################################
    
    
    def PlaceOrder(self, Exchange, TrdSymbol, OrderQty, OrderPrice, BuyOrSell, AccountId, OrderValidity = 'DAY', OrderPriceType = 'L', OrderProductType = 'NRML', OrderByCustFirm = 'C'):
        """
        Function to place a new order in the Exchange. 
        
        Parameters
        ----------
        Exchange : string
            The symbol of the Exchange in lower case
        
        TrdSymbol : string
            The trading symbol of the stock
        
        OrderQty : integer
            The order quantity. Must be greater than 0.
        
        OrderPrice : float
            The order price. Must be greater than 0.
        
        BuyOrSell : string
            The transaction, 'B' for buying or 'S' for selling
        
        AccountId : string, optional
            The trading account ID. Default is None
        
        OrderValidity : string, optional
            The validity time of the order, 'DAY' or 'IOC' or 'GTD' Good Till Days or 'GTC' for Good Till Cancel.
            The default is 'DAY'
        
        OrderPriceType : string, optional
            The order price type, 'L' for LIMIT order or 'MKT' for MARKET order or 'SL' for STOP LOSS order 
            or 'SL-M' for STOP LOSS MARKET order. The default is 'L'
        
        OrderProductType : string, optional
            The type of order, 'NRML' for NORMAL order  or 'MIS' for MARGIN trading order or 'CNC' for DELIVERY order
            or 'ARB' for ARBITRAGE order. The default is 'NRML'
        
        OrderByCustFirm : string, optional
            The order placed by Customer 'C' or Firm 'F'. The default is 'C'
         
         
        Returns
        ----------
        GUIOrderID : string
            Returns the GUIOrderID if Jupitron Server could place the order, else returns nothing
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            if (Exchange.strip() == '' or TrdSymbol.strip() == '' or OrderQty <= 0 or OrderPrice < 0 or BuyOrSell.strip() == '' or (BuyOrSell != 'B' and BuyOrSell != 'S') or AccountId.strip() == ''):
                return {'Input Error' : 'One or more mandatory parameters not specified properly'}
            
            request = 'PLACE_ORDER_NEST' + '\n' + Exchange + '\n' + TrdSymbol + '\n' + str(OrderQty) + '\n' + str(OrderPrice) + '\n' + BuyOrSell + '\n' + AccountId + '\n' + OrderValidity + '\n' + OrderPriceType + '\n' + OrderProductType + '\n' + OrderByCustFirm
            response = self.__GetDataFromJupitron(request)
            if (response == None or response == '' or response == '14'):
                return None
            response = {'GUIOrderID' : response}
        except:
            response = None
        
        return response
    #############################################################################################################
    
    
    def ModifyOrder(self, GUIOrderID, NestOrderID, Exchange, OrderQty, OrderPrice, OrderValidity = 'DAY', OrderPriceType = 'L'):
        """
        Function to modify an existing Open order in the Exchange. 
        
        Parameters
        ----------
        GUIOrderID : string
            The GUIOrderID of the order
        
        NestOrderID : string
            The NestOrderID of the order
        
        Exchange : string
            The symbol of the Exchange in lower case
        
        OrderQty : integer
            The order quantity. Must be greater than 0.
        
        OrderPrice : float
            The order price. Must be greater than 0.
        
        OrderValidity : string, optional
            The validity time of the order, 'DAY' or 'IOC' or 'GTD' Good Till Days or 'GTC' for Good Till Cancel.
            The default is 'DAY'
        
        Returns
        ----------
        ReturnCode : string
            Returns a number specifying the result of the operation
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            if (Exchange.strip() == '' or GUIOrderID.strip() == '' or NestOrderID.strip() == '' or OrderQty <= 0 or OrderPrice < 0):
                return {'Input Error' : 'One or more mandatory parameters not specified properly'}
            request = 'MODIFY_ORDER_NEST' + '\n' + GUIOrderID + '\n' + NestOrderID + '\n' + Exchange  + '\n' + str(OrderQty) + '\n' + str(OrderPrice) + '\n' + OrderValidity + '\n' + OrderPriceType
            response = self.__GetDataFromJupitron(request)
            if (response == None or response == '' or response == '14'):
                response = {'Status' : 'Modify failed'}
            else:
                response = {'Status' : 'Order modified'}
        except:
            response = None
        
        return response
    #############################################################################################################
    
    
    def CancelOrder(self, GUIOrderID, NestOrderID):
        """
        Function to cancel an existing Open order in the Exchange. Only the balance Unfilled quantities will be
        cancelled
        
        Parameters
        ----------
        GUIOrderID : string
            The GUIOrderID of the order
        
        NestOrderID : string
            The NestOrderID of the order
        
        Returns
        ----------
        ReturnCode : string
            Returns a number specifying the result of the operation
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            if (GUIOrderID.strip() == '' or NestOrderID.strip() == ''):
                return {'Input Error' : 'GUIOrderID mandatory parameter not specified properly'}
            request = 'CANCEL_ORDER_NEST' + '\n' + GUIOrderID + '\n' + NestOrderID
            response = self.__GetDataFromJupitron(request)
            if (response == None or response == '' or response == '14'):
                response = {'Status' : 'Cancel failed'}
            else:
                response = {'Status' : 'Order cancelled'}
            
        except:
            response = None
        
        return response
    #############################################################################################################
    
    
    def GetOrderStatus(self, GUIOrderID):
        """
        Function to get the status of a placed order. Returns a dictionary object. 
        
        Parameters
        ----------
        GUIOrderID : string
            The GUIOrderID of the order
        
        Returns
        ----------
        GuiOrdId : string
            GUI Order ID
        
        NestOrdNum : string
            NEST Order ID
        
        ExchOrdId : string
            Exchange Order ID
        
        QuanToFill : integer
            Total Order Quantity
        
        FilledShares : integer
            Filled Quantity
        
        UnfilledSize : integer
            Unfilled Quantity
        
        CancelledSize : integer
            Cancelled Quantity
        
        Price : float
            Order Price
        
        AvgPrice : float
            Avg Price
        
        NestUpdateTime : string
            Nest Update Time
        
        ExchTime : string
            Exchange Time
        
        ExchOrdUpdateTime : string
            Exchange Order UpdateTime
        
        Status : string
            Status
        
        OrdStatus : string
            Order Status
        
        RejReason : string
            Rejection Reason
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            if (GUIOrderID.strip() == ''):
                return {'Input Error' : 'GUIOrderID mandatory parameter not specified properly'}
            request = 'GET_ORDER_STATUS_NEST' + '\n' + GUIOrderID 
            response = self.__GetDataFromJupitron(request)
            if (response == None or response == '' or response == '14'):
                return None
            response = response.split('|')
            
            keys = ['GUIOrdID', 'NestOrdNum', 'ExchOrdId', 'Exchange', 'TrdSymbol', 'TransType', 'QuanToFill', 
                    'FilledShares', 'UnfilledSize', 'CancelledSize', 'Price', 'AvgPrice', 'NestUpdateTime', 
                    'ExchTime', 'ExchOrdUpdateTime', 'Status', 'OrdStatus', 'RejReason']
            
            responsedict = {}
            for i in range(len(keys)):
                responsedict.update({keys[i] : response[i]})
            
            response = responsedict
        except:
            response = None
        
        return response
    #############################################################################################################
    
    
    def GetOrderHistory(self):
        """
        Function to get the details of all the placed order. Returns a Pandas DataFrame. 
        
        Returns
        ----------
        GuiOrdId : string
            GUI Order ID
        
        NestOrdNum : string
            NEST Order ID
        
        ExchOrdId : string
            Exchange Order ID
        
        ExchSeg : string
            Exchange
        
        TrdSymbol : string
            Trade Symbol
        
        Symbol : string
            Symbol
        
        Price : float
            Order Price
        
        Quantity : integer
            Order Quantity
        
        TransType : string
            Transaction Type B/S
        
        AvgPrice : float
            Avg Price
        
        FilledShares : integer
            Filled Quantity
        
        UnfilledSize : integer
            Unfilled Quantity
        
        Status : string
            Status
        
        RejReason : string
            Rejection Reason
        
        ExchTime : string
            Exchange Time
        
        FillTime : string
            Fill Time
        
        Product : string
            Product
        
        AccountId : string
            AccountId
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            request = 'GET_ORDER_HISTORY_NEST' 
            response = self.__GetDataFromJupitron(request, True)
            if (response == None or response == '' or response == '14'):
                return None
            
            response = response.split('\n')
            
            columns = response[0].split('|')
            data = []
            for i in range(1, len(response)):
                fields = response[i].split('|')
                data.append(fields)
            
            df = pd.DataFrame(data, columns=columns)
            
            return df
        except:
            return None
        
    #############################################################################################################
    
    
    def GetTradeHistory(self):
        """
        Function to get the details of all the trades. Returns a Pandas DataFrame.
        
        Returns
        ----------
        GuiOrdId : string
            GUI Order ID
        
        NestOrdNum : string
            NEST Order ID
        
        ExchOrdId : string
            Exchange Order ID
        
        ExchSeg : string
            Exchange
        
        TrdSymbol : string
            Trade Symbol
        
        Symbol : string
            Symbol
        
        FillPrice : float
            Traded price
        
        FillSize : integer
            Traded Quantity
        
        TransType : string
            Transaction Type B/S
        
        FillLeg : string
            Fill Leg
        
        FillStatus : string
            Fill Status
        
        Status : string
            Status
        
        ExchTime : string
            Exchange Time
        
        FillTime : string
            Fill Time
        
        Product : string
            Product
        
        AccountId : string
            AccountId
                
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            request = 'GET_TRADE_HISTORY_NEST' 
            response = self.__GetDataFromJupitron(request, True)
            if (response == None or response == '' or response == '14'):
                return None
            
            response = response.split('\n')
            
            columns = response[0].split('|')
            data = []
            for i in range(1, len(response)):
                fields = response[i].split('|')
                data.append(fields)
            
            df = pd.DataFrame(data, columns=columns)
            
            return df
        except:
            return None
    #############################################################################################################
    
    
    def GetErrorMessages(self):
        """
        Function to get all the error messages from the Jupitron Server.
        
        Returns
        ----------
        ErrorMessages : list
            Returns a list of all the error messages since the last read.
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            request = 'GET_ERROR_MESSAGES' 
            response = self.__GetDataFromJupitron(request, True)
            if (response == None or response == '' or response == '14'):
                return None
            response = response.split('\n')
        except:
            response = None
        
        return response
    #############################################################################################################
    
    
    def GetMasterData(self, Exchange):
        """
        Function to get the master data of instruments for an exchange.
        
        Returns
        ----------
        MasterData : list
            Returns a list of master data of instruments.
        
        Raises
        ------
        NotImplementedError
            If no parameter is passsed.
            
        """
        
        try:
            if (Exchange.strip() == ''):
                return {'Input Error' : 'One or more mandatory parameters not specified properly'}
            request = 'GET_MASTER_DATA' + '\n' + Exchange
            response = self.__GetDataFromJupitron(request, True)
            if (response == None or response == '' or response == '14'):
                return None
            response = response.split('\r\n')
        except:
            response = None
        
        return response
    #############################################################################################################




a = Jupitron()
print(a.Login('iiqfstudent', 'iiqf*#123'))
b = a.GetQuote('nse_fo', 'BAJFINANCE')
print(b)
