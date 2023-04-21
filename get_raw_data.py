import logging
import requests
import json
from datetime import datetime,date
from config.config import APIkeys, DBInfo
from model import bulk_insert, get_all

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_raw_data(symbol: str) -> json:
    """
    Return json object of financial data by given symbol.
    If Exception, exit'
    """
    try:
        query_params={
                        'function':"TIME_SERIES_DAILY_ADJUSTED", 
                        'symbol':symbol, 
                        'outputsize':'compact',
                        'apikey': APIkeys.AlphaVintageAPIKeySecret
                     }
        url = f'https://www.alphavantage.co/query'
        r = requests.get(url, params=query_params)
        return r.json()
    except Exception as e:
        SystemExit(e)

def process_raw_data(symbol: str) -> list:
    """
    Return list of financial data objects by given symbol.
    If Exception, exit'
    """
    try:
        financial_data = []
        data = fetch_raw_data(symbol)
        ts_data=data.get('Time Series (Daily)', {})
        if not ts_data:
            raise Exception('Could not find time series data')
        
        for key, value in ts_data.items():
            today = date.today()
            old_date = datetime.strptime(key, "%Y-%m-%d").date()
            delta = today - old_date
            
            if int(delta.days) <= 14:
                data_object = {
                        "symbol": symbol,
                        "date": old_date,
                        "open_price": value.get('1. open'),
                        "close_price": value.get('4. close'),
                        "volume": value.get('6. volume'),
                    }
                financial_data.append(data_object)
                logging.info(today)
                logging.info(old_date)
                logging.info(f'Difference is {delta.days} days')
        return financial_data
    except Exception as e:
        SystemExit(e)

def main():
    symbols = ["IBM", "AAPL"]
    for symbol in symbols:
        bulk_insert(process_raw_data(symbol), DBInfo.DatabaseURLLocal)
    data = get_all(DBInfo.DatabaseURLLocal)
    logging.info(data)

main()
