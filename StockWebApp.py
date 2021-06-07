import datetime
from yahoo_fin import stock_info
import pandas as pd
import pandas_datareader as web
from PIL import Image
import streamlit as stt
from companyNameSymbol import *


stt.sidebar.header('User Input')

# function to get user input

def get_input():
    end_date = stt.sidebar.date_input("End Date",datetime.datetime.today()-datetime.timedelta(days=1),max_value=datetime.datetime.today())
    start_date = stt.sidebar.date_input("Start Date",end_date-datetime.timedelta(days=2),min_value=datetime.date(end_date.year-20,1,1),max_value=end_date)

    #choice = stt.sidebar.selectbox("Menu", menu)
    stock_symbol = stt.sidebar.selectbox("Stock Symbol", menu)
    return start_date, end_date, stock_symbol

# function for getting company name
def get_company_name(symbol):

    if symbol in Company:
        return Company[symbol]
    else:
        'None'


# fun for proper company name and proper date
def get_data(symbol, start, end):
    path_out= "D:/python project/Stock-Representation-WebApp-py-/Stocks/"
    df=pd.read_csv(path_out+symbol+'.csv')

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

    if start <= end:
        end_date = datetime.datetime.today()
        start_date = datetime.date(end_date.year - 20, 1, 1)

        symbol = symbol.upper()
        symbol1 = get_company_name(symbol)
        try:
            uf = web.DataReader(symbol1, 'yahoo', start, end)
            path_out = 'D:/python project/Stock-Representation-WebApp-py-/Stocks/'
            uf.to_csv(path_out + symbol1 + '.csv')

            df = get_data(symbol1, start, end)
            company_name = get_company_name(symbol.upper())

            stt.header(
                symbol + "'s Latest Stock Price " + str("{:.2f}".format(stock_info.get_live_price(symbol1))) + '$')

            stt.header(symbol.upper() + " Close Price\n")
            stt.line_chart(df['Close'])

            stt.header(symbol.upper() + " Volume\n")
            stt.line_chart(df['Volume'])

            stt.header('Data Statistics')
            stt.write(df.describe())
        except:
            stt.error("Data Unavailable")

    else:
        stt.error("Please Choose Correct Duration")

