# -*- coding: utf-8 -*-
"""
Created on Thu May  6 10:01:32 2021

@author: User1
"""
import csv
import pandas as pd
import numpy as np
import os
import sys


def read_csv_to_list(file_name):
    try:
        if not (os.path.isfile(file_name)):
            return None
        
        data = []
        with open(file_name, 'r') as myfile:
            reader = csv.reader(myfile, delimiter=',', quotechar = '"', lineterminator = '\n')
            for row in reader:
                data.append(row)
            myfile.close()
        return data
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None

def write_list_to_csv(file_name, data):
    """
    data : Must be a 2-D List
    """
    try:
        with open(file_name, 'w', newline='') as myfile:
            writer = csv.writer(myfile, delimiter=',', lineterminator = '\n')
            for row in data:
                writer.writerow(row)
            myfile.close()
        return True
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return False
    
        
def read_csv_to_array(file_name):
    try:
        if not (os.path.isfile(file_name)):
            return np.empty(0)
        
        data = np.array(read_csv_to_list(file_name))
        return data
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return np.empty(0)
    

def write_array_to_csv(file_name, data):
    """
    data : Must be a 2-D Array
    """
    return write_list_to_csv(file_name, data)


def read_dataframe(file_name):
    try:
        if not (os.path.isfile(file_name)):
            return pd.DataFrame()
        
        data = pd.read_csv(file_name)
        return data
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return pd.DataFrame()


def write_dataframe(file_name, data, saveindexcol = True):
    """
    data : Must be a pandas dataframe
    """
    try:
        data.to_csv(file_name + '.csv', index = saveindexcol)
        return True
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return False

def read_data_to_string(file_name):
    try:
        if not (os.path.isfile(file_name)):
            return None
        
        with open(file_name, 'r') as myfile:
            data = myfile.read()
            myfile.close()
        return data
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None

def write_string_to_file(file_name, data):
    try:
        with open(file_name, 'w') as myfile:
            myfile.write(data)
            myfile.close()
        
        return True
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return False
    

def read_data(file_name):
    try:
        if not (os.path.isfile(file_name)):
            return None
        
        with open(file_name, 'r') as myfile:
            data = myfile.readlines()
            myfile.close()
        return data
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return None

def write_data(file_name, data, addnewline = True):
    try:
        data = np.array(data)
        with open(file_name, 'w', newline='') as myfile:
            for row in data:
                if type(row) != list and addnewline:
                    row = row + '\n'
                myfile.writelines(row)
            myfile.close()
        
        return True
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return False

def write_binary_data(file_name, data):
    try:
        data = np.array(data)
        with open(file_name, 'wb') as myfile:
            myfile.write(data)
            myfile.close()
        
        return True
    except:
        return False


def read_stock_data(stock_name, input_path):
    try:
        file_name = input_path + '/' + stock_name + ".csv"
        if not (os.path.isfile(file_name)):
            return pd.DataFrame()
        
        data = pd.read_csv(file_name)
        data = data[['Date','Close']]
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index(keys='Date')
        return data
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return pd.DataFrame()


def read_stock_OHLCdata(stock_name, input_path):
    try:
        file_name = input_path + '/' + stock_name + ".csv"
        if not (os.path.isfile(file_name)):
            return pd.DataFrame()
        
        data = pd.read_csv(file_name)
        data = data[['Date','Open','High','Low','Close']]
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index(keys='Date')
        return data
    except Exception as ex:
        print(sys._getframe().f_code.co_name, 'exception :', ex)
        return pd.DataFrame()



