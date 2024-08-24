from credentials.SeldonDBCredentials import *
from credentials.EodHistoricalDataCredentials import *
import pandas as pd
import requests


url = f'https://eodhd.com/api/exchanges-list/?api_token={eod_api}&fmt=json'
exc_data = requests.get(url).json()
data = pd.DataFrame(exc_data)
print(data.iloc[1])
data.to_csv('test_spot/exchanges.csv', index=False)


url = f'https://eodhd.com/api/exchange-symbol-list/{'NYSE'}?api_token={eod_api}&fmt=json'
exc_data = requests.get(url).json()
data = pd.DataFrame(exc_data)
print(data.iloc[1])
data.to_csv('test_spot/tickers.csv', index=False)