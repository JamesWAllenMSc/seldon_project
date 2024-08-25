import toolkit
import credentials as access
import logging
import pandas as pd


# Test ticker retrieval
ticker_data = toolkit.retrieve_tickers(access.eodhd_api, 'NYSE')
# print(ticker_data)


# Test 'exchange_retrieval'
exchange_data = toolkit.retrieve_exchanges(access)
# print(exchange_data)


# Test 'execute_query'
# execute_query = 'CREATE TABLE Persons (PersonID int, LastName varchar(255), FirstName varchar(255), Address varchar(255), City varchar(255));'
# execute_query = 'DROP TABLE Persons'
# toolkit.execute_query(access, execute_query)

# Test 'retrieve_table'
retrieve_table_query = 'SELECT * FROM Persons'
table = toolkit.retrieve_table(access, retrieve_table_query)
table = pd.DataFrame(table)
print(table.columns)


