import toolkit
import credentials as access
import logging
import pandas as pd
import numpy as np
import requests

# Logging config
logging.basicConfig(filename='logs/global_event.log', level=logging.INFO,
                        format='Datetime:%(asctime)s - Level:%(levelname)s - Module:%(module)s - Function:%(funcName)s - Message:%(message)s')

"""
# Test ticker retrieval
ticker_data = toolkit.retrieve_tickers(access.eodhd_api, 'NYSE')
print(ticker_data)
"""

"""
# Test 'exchange_retrieval'
exchange_data = toolkit.retrieve_exchanges(access.eodhd_api)
print(exchange_data)
"""

"""
# Test 'execute_query'
execute_query = 'CREATE TABLE Persons (PersonID int, LastName varchar(255), FirstName varchar(255), Address varchar(255), City varchar(255));'
execute_query = 'DROP TABLE Persons'
toolkit.execute_query(access, execute_query)
"""

"""
# Test 'retrieve_table'
retrieve_table_query = 'SELECT * FROM global_exchanges;'
db_columns = ['Name', 'Code', 'OperatingMIC', 'Country', 
              'Currency', 'CountryISO2', 'CountryISO3']
table = toolkit.retrieve_table(access, retrieve_table_query)
table = pd.DataFrame(table, columns=db_columns)
logging.info(f"Exchanges update complete.")
print(table)
"""

"""
exchange_data = toolkit.retrieve_exchanges(access.eodhd_api)
# Workaround for EodHD grouping stock listings
# Remove USA stocks from EodHD exchenge data
exchange_data = exchange_data[exchange_data['Name'] != 'USA Stocks'] 
# Manually enter US exchanges
us_stocks = pd.DataFrame.from_dict({
    'Name':['New York Stock Exchange', 'NASDAQ'],
    'Code':['NYSE', 'NASDAQ'],
    'OperatingMIC':['XNYS', 'XNAS'],
    'Country':['US', 'US'],
    'Currency':['USD', 'USD'],
    'CountryISO2':['US', 'US'],
    'CountryISO3':['USA', 'USA']
})
exchange_data = pd.concat([exchange_data, us_stocks], ignore_index=True)
exchange_data_columns = exchange_data.columns.values
exchange_data = exchange_data.replace({np.nan:'None'})
exchange_data = str(exchange_data.values.tolist())
exchange_data = exchange_data.replace('[', '(').replace(']', ')')
exchange_data = exchange_data[1:-1]

columns = ', '.join(exchange_data_columns)

add_record_query = f'INSERT INTO global_exchanges ({columns}) VALUES {exchange_data};'
toolkit.execute_query(access, add_record_query)


#add_record_query = f'INSERT INTO global_exchenges ({columns}) VALUES {exchange_data};'
#toolkit.execute_query(access, add_record_query)
"""
