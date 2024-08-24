import logging
import pandas as pd

url = f'https://eodhistoricaldata.com/api/exchange-symbol-list/{'NYSE'}?api_token={'66b663608c1730.26105339'}'

response = pd.read_csv(url)

print(response)

response.to_csv('test_spot/tickers.csv', index=False)