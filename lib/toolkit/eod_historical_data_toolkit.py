import pandas as pd
import requests
import logging


def retrieve_tickers(eodhd_api, exchange):
    """ Takes api credentials for eodhd.com and a target exchange and returns a pandas dataframe containing 
    all tickers from the target exchange
    """
    url = f'https://eodhd.com/api/exchange-symbol-list/{exchange}?api_token={eodhd_api}&fmt=json'
    try:
        ticker_data = requests.get(url).json()
        ticker_data = pd.DataFrame(ticker_data)
        return ticker_data
    except Exception as e:
        logging.error(e)


def retrieve_exchanges(eodhd_api):
    """ Takes api credentials for eodhd.com and returns full list of available exchanges
    """
    try:
        url = f'https://eodhd.com/api/exchanges-list/?api_token={eodhd_api}&fmt=json'
        exc_data = requests.get(url).json()
        exc_data = pd.DataFrame(exc_data)
        return(exc_data)
    except Exception as e:
        logging.error(e)