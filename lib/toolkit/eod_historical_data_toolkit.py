import pandas as pd
import requests
import logging
import datetime



def retrieve_tickers(eodhd_api, exchange):
    """ Takes api credentials for eodhd.com and a target exchange and returns a pandas dataframe containing 
    all tickers from the target exchange
    """
    url = f'https://eodhd.com/api/exchange-symbol-list/{exchange}?api_token={eodhd_api}&fmt=json'
    try:
        ticker_data = requests.get(url).json()
        ticker_data = pd.DataFrame(ticker_data)
        ticker_data['Source'] = 'EoDHD.com' # Adds Source column
        ticker_data['Date_Updated'] = datetime.datetime.now() # Adds timestamp
        id = ticker_data['Code']+ticker_data['Exchange']
        ticker_data['Ticker_ID'] = id
        ticker_columns = ['Ticker_ID', 'Code', 'Name', 'Country', 'Exchange',
                        'Currency', 'Type', 'Isin', 'Source',
                        'Date_Updated']
        ticker_data = ticker_data[ticker_columns]
        return ticker_data
    except Exception as e:
        logging.error(f'Exchange: {exchange} -  {e}', exc_info=True)
    
   
             

def retrieve_exchanges(eodhd_api):
    """ Takes api credentials for eodhd.com and returns full list of available exchanges
    """
    try:
        url = f'https://eodhd.com/api/exchanges-list/?api_token={eodhd_api}&fmt=json'
        exc_data = requests.get(url).json()
        exc_data = pd.DataFrame(exc_data)
        exc_data = exc_data[exc_data['Name'] != 'USA Stocks'] # Removing grouped US stocks
        exc_data['Source'] = 'EoDHA.com' # Adds Source column
        exc_data['Date_Updated'] = datetime.datetime.now() # Adds timestampus_stocks = pd.DataFrame.from_dict({
        # Add in individual US exchanges
        us_stocks = pd.DataFrame.from_dict({
            'Name':['New York Stock Exchange', 'NASDAQ'],
            'Code':['NYSE', 'NASDAQ'],
            'OperatingMIC':['XNYS', 'XNAS'],
            'Country':['US', 'US'],
            'Currency':['USD', 'USD'],
            'CountryISO2':['US', 'US'],
            'CountryISO3':['USA', 'USA'],
            'Source':['Manual_Input', 'Manual_Input'],
            'Date_Updated':[datetime.datetime.now(), datetime.datetime.now()]
        })
        exc_data = pd.concat([exc_data, us_stocks], ignore_index=True)
        return(exc_data)
    except Exception as e:
        logging.error(e, exc_info=True)
    