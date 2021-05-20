import streamlit as st
import pandas as pd
from PIL import Image
import subprocess

subprocess.call(['StockWebApp.py'], shell=True)

# Add title and image
st.write("""
# Stock Market Web Application
**Visually** show data on Stock,Data range from 8 May 2020 - 7 May 2021
""")

image = Image.open("D:/python project/Stock-Representation-WebApp-py-/Asserts/StMaWebApp.jpg")
st.image(image,use_column_width=True)

# Create a sidebar header
st.sidebar.header('User Input')

# function to get user input

def get_input():
    start_date = st.sidebar.text_input("Start Date","2020-05-08")
    end_date = st.sidebar.text_input("End Date", "2021-05-07")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AMZN")
    return start_date, end_date, stock_symbol

# function for getting company name
def get_company_name(symbol):
    if symbol=="AMZN":
        return "Amazon"
    elif symbol=="TSLA":
        return "Tesla"
    elif symbol=="GOOG":
        return "Alphabate"
    else:
        'None'

# fun for proper company name and proper date
def get_data(symbol, start, end):
    if symbol.upper()=='AMZN':
        df= pd.read_csv("D:/python project/Stock-Representation-WebApp-py-/Stocks/AMZN.csv")
    elif symbol.upper()=='TSLA':
        df= pd.read_csv("D:/python project/Stock-Representation-WebApp-py-/Stocks/TSLA.csv")
    elif symbol.upper()=='GOOG':
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
        if end<= pd.to_datetime(df['Date'][len(df)-1-j]):
            end_row= len(df)-1-j
            break

    # set the index to be the date
    df=df.set_index(pd.DatetimeIndex(df['Date'].values))

    return  df.iloc[start_row: end_row +1,]


start,end,symbol = get_input()

df=get_data(symbol,start,end)

company_name=get_company_name(symbol.upper())

st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])

st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

st.header('Data Statistics')
st.write(df.describe())
