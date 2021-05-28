import streamlit as stt
import pandas as pd
from PIL import Image
import subprocess
import pandas_datareader as web
import datetime

#subprocess.call(['StockWebApp.py'], shell=True)

# Add title and image


# Create a sidebar header
stt.sidebar.header('User Input')

# function to get user input

def get_input():
    start_date = stt.sidebar.text_input("Start Date","2020-05-08")
    end_date = stt.sidebar.text_input("End Date", "2021-05-07")
    stock_symbol = stt.sidebar.text_input("Stock Symbol", "AMAZON")
    return start_date, end_date, stock_symbol

# function for getting company name
def get_company_name(symbol):
    if symbol=="AMAZON":
        return "AMZN"
    elif symbol=="TESLA":
        return "TSLA"
    elif symbol=="GOOGLE":
        return "GOOG"
    else:
        'None'

# fun for proper company name and proper date
def get_data(symbol, start, end):
    if symbol.upper()=='AMAZON':
        df= pd.read_csv("D:/python project/Stock-Representation-WebApp-py-/Stocks/AMZN.csv")
    elif symbol.upper()=='TESLA':
        df= pd.read_csv("D:/python project/Stock-Representation-WebApp-py-/Stocks/TSLA.csv")
    elif symbol.upper()=='GOOGLE':
        df= pd.read_csv("D:/python project/Stock-Representation-WebApp-py-/Stocks/GOOG.csv")
    else:
        df= pd.DataFrame(columns=['Date','Open','High','Low','Close','Adj Close','Volume'])

    # Get the data range
    start=pd.to_datetime(start)
    end=pd.to_datetime(end)

    # Start and End Index
    start_row=0
    end_row=0

    # start date (user input)
    for i in  range(0,len(df)):
        if start<= pd.to_datetime(df['Date'][i]):
            start_row=i
            break

    # End date (user data)
    for j in  range(0,len(df)):
        if end >= pd.to_datetime(df['Date'][len(df)-1-j]):
            end_row= len(df)-1-j
            break

    # set the index to be the date
    df=df.set_index(pd.DatetimeIndex(df['Date'].values))

    return  df.iloc[start_row: end_row +1,]

def startup():

    # Create a sidebar header
    stt.sidebar.header('User Input')
    start,end,symbol = get_input()

    end_date = datetime.datetime.today()
    start_date = datetime.date(end_date.year-20,1,1)

    symbol1=get_company_name(symbol)
    uf = web.DataReader(symbol1, 'yahoo', start_date, end_date)

    path_out = 'D:/python project/Stock-Representation-WebApp-py-/Stocks/'
    uf.to_csv(path_out +symbol1+'.csv')

    df=get_data(symbol,start,end)

    company_name=get_company_name(symbol.upper())

    stt.header(symbol.upper()+" Close Price\n")
    stt.line_chart(df['Close'])

    stt.header(symbol.upper()+" Volume\n")
    stt.line_chart(df['Volume'])

    stt.header('Data Statistics')
    stt.write(df.describe())
