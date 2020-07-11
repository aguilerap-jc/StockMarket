#Data processing libraries
import numpy as np
import pandas as pd

#Finance Data libraries
import tiingo
import quandl
import iexfinance
import intrinio_sdk
import alpha_vantage
import yfinance as yf
from yahoofinancials import YahooFinancials

#Personal libraries
import usr_lib.get_apikeys as get_apikeys

#Time handler
from datetime import date

DEFAULT_START_DATE = "2016-01-01"
DEFAULT_END_DATE = date.today().strftime("%Y-%m-%d")

QUANDL_KEY = get_apikeys.get_api_key("quandl")
quandl.ApiConfig.api_key = QUANDL_KEY

INTRINIO_KEY = get_apikeys.get_api_key("intrinio")
intrinio_sdk.ApiClient().configuration.api_key["api_key"] = INTRINIO_KEY
security_api = intrinio_sdk.SecurityApi()

IEXFINANCE_KEY = get_apikeys.get_api_key("iexfinance")

TIINGO_KEY = get_apikeys.get_api_key("tiingo")
tiingo_client = tiingo.TiingoClient({"session":True,"api_key":TIINGO_KEY})
 
ALPHAVANTAGE_KEY = get_apikeys.get_api_key("alphavantage")


def get_stock_yf(stock='TSLA',start_date=DEFAULT_START_DATE,end_date=DEFAULT_END_DATE):
    stock_df = yf.download(stock, 
                      start=start_date, 
                      end=end_date, 
                      progress=False)
    return stock_df

def get_stock_quandl(stock='AAPL',db = "WIKI",start=DEFAULT_START_DATE,end=DEFAULT_END_DATE):
    ds = db+"/"+stock
    df_quandl = quandl.get(dataset=ds,
                           start_date=start,
                           end_date=end)
    return df_quandl

def get_stock_intrinio(id="AAPL",start=DEFAULT_START_DATE,end=DEFAULT_END_DATE,freq="daily",page_s=10000):
    r = security_api.get_security_stock_prices(identifier=id,
                                               start_date=start,
                                               frequency=freq,
                                               page_size=page_s)
    #Structure the data as a dataframe
    response_list = [x.to_dict() for x in r.stock_prices]
    df_int = pd.DataFrame(response_list).sort_values("date")
    df_int.set_index("date",inplace=True) 
    return df_int
    
def get_stock_iexfinance(stock="AAPL",start=DEFAULT_START_DATE,end=DEFAULT_END_DATE,output_form="pandas"):
    from iexfinance.stocks import get_historical_data
    
    df_iex = get_historical_data(stock,
                                 start,
                                 end,
                                 output_format=output_form,
                                 token=IEXFINANCE_KEY)
    return df_iex
    
def get_stock_tiingo(stock="AAPL",start=DEFAULT_START_DATE,end=DEFAULT_END_DATE):
    
    historical_p = tiingo_client.get_dataframe(stock, 
                                               startDate=start, 
                                               endDate=end,
                                               frequency="daily")
    return historical_p

def get_stock_alpha_vantage(stock="AAPL",start=DEFAULT_START_DATE,end=DEFAULT_END_DATE):
    from alpha_vantage.timeseries import TimeSeries
    
    ts = TimeSeries(key=ALPHAVANTAGE_KEY, output_format="pandas")
    
    data, meta_data = ts.get_intraday(symbol=stock,
                                      interval='1min', 
                                      outputsize='full')
    return data
