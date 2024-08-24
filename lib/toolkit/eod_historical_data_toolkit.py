import pandas as pd


def retrieve_tickers(access_key, exchange):
    """ Takes api credentials for eodhistoricaldata.com and a target exchange and returns a pandas dataframe containing 
    all tickers from the target exchange
    """
    url = f'https://eodhistoricaldata.com/api/exchange-symbol-list/{exchange}?api_token={access_key}'
    try:
        response = pd.read_csv(url)
        return response
    except Exception as e:
        print(e)