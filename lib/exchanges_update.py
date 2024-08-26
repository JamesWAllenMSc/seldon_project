"""This function retrieves the exchanges list held on the database and
compares it to the list of exchanges held on EodHD.com. Any that are
missing are added to the database.
"""

import toolkit
import credentials as access
import logging
import pandas as pd

# Logging config REQUIRED FOR DEV,REMOVE AT DEPLOYMENT
logging.basicConfig(filename='logs/global_event.log', level=logging.INFO,
                        format='Datetime:%(asctime)s - Level:%(levelname)s - Module:%(module)s - Function:%(funcName)s - Message:%(message)s')


# RETRIEVE EXCHANGE DATA FROM SERVER
retrieve_table_query = 'SELECT * FROM global_exchanges;'

# Declare columns for database
db_columns = ['Name', 'Code', 'OperatingMIC', 'Country', 
              'Currency', 'CountryISO2', 'CountryISO3']
# Run query retrieving database with declared column names
db_exchange_data = toolkit.retrieve_table(access, retrieve_table_query)
db_exchange_data = pd.DataFrame(db_exchange_data, columns=db_columns)
print('-' * 100)
print('Table from Server')
print(db_exchange_data)
print('-' * 100)

# RETRIEVE EXCHANGE LIST FROM EOD.COM
eod_exchange_data = toolkit.retrieve_exchanges(access.eodhd_api)
print('EODData')
print(eod_exchange_data)
print('-' * 100)
logging.info(f"Exchanges update complete.")

# JOIN DATAFRAMES LEAVING JUST THOSE THAT ARE MISSING FROM SELDON DATABASE
