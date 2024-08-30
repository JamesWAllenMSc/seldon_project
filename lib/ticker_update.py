"""This script takes the exchanges from seldon_db and iterates over the exchange codes updating 
the list of tickers held on the database. 
"""

import toolkit
import credentials as access
import logging
import toolkit
import pandas as pd
import numpy as np
import time


# RETRIEVE EXCHANGE CODES HELD ON SELDON_DB




# RETRIEVE TICKERS HELD ON SELDON_DB
table_query = 'SELECT Code FROM global_tickers;'
col_name = ['Code', 'Name', 'Country', 'Exchange',
            'Currency', 'Type', 'Isin', 'Source',
            'Date_Updated']
table = toolkit.retrieve_table(access, table_query)
ticker_list = pd.DataFrame(table, columns=col_name)
logging.debug(f"Tickers retrieved from seldon_db.global_tickers")

# ITERATE OVER SELDON_DB EXCHANGE CODE LIST 
# AND USE THIS TO RETIEVE LIST OF TICKERS HELD
# ON EODHD.COM FOR EACH EXCHANGE
#for code in exchange_list:
 #   ticker_data_eod = toolkit.retrieve_tickers(access.eodhd_api, code) # Gets ticker list according to exchenge
    #ticker_data_seldon_db = 
    #stacked_ = pd.concat([eod_exchange_codes, db_exchange_codes], axis=0) # Create series of all codes
    #print(ticker_data)


# START RIGHT HERE!!!!!

# GET EXCHANGES LIST FROM SELDON_DB
table_query = 'SELECT Code FROM global_exchanges;'
col_name = ['Code']
table = toolkit.retrieve_table(access, table_query)
table = pd.DataFrame(table, columns=col_name)
exchange_list = table['Code'].to_list()
logging.debug(f"Exchanges retrieved from seldon_db.global_exchenges")


# ITERATE OVER EXCHANGES LIST RETRIEVING TICKERS FOR EACH EXCHANGE 
# ON BOTH SELDON_DB AND EODHD.COM
for exchange_code in exchange_list:
    # Rquest ticker list from seldon_db filtered by exchange code
    table_query = f"SELECT * FROM global_tickers WHERE Exchange='{exchange_code}';"
    db_columns = ['Code', 'Name', 'Country', 'Exchange',
                'Currency', 'Type', 'Isin', 'Source',
                'Date_Updated']
    table = toolkit.retrieve_table(access, table_query)
    ticker_data_db = pd.DataFrame(table, columns=db_columns)
    logging.debug(f"Tickers retrieved from seldon_db.global_tickers")
    
    # Request ticker codes from eodhd.com filtered by exchange code
    ticker_data_eod = toolkit.retrieve_tickers(access.eodhd_api, exchange_code) # Gets ticker list according to exchenge
    logging.debug(f"Data retrieved from EoDHD.com")

    # CHECK THERE ARE NO CHANGES TO HEADERS
    logging.debug("Checking header changes")
    headers_eod = ticker_data_eod.columns.values
    db_col_array = np.array(db_columns)

    if np.array_equal(headers_eod, db_col_array):
        logging.debug(f"EodHD / Seldon_DB header check: COMPLETE")
    else:
        logging.error(f"EodHD / Seldon_DB column check: FAILED")
        exit

    # FILTER TICKER CODES MISSING FROM SELDON_DB 
    eod_ticker_codes = ticker_data_eod['Code'] # Isolate codes from EoDHD.com
    db_ticker_codes = ticker_data_db['Code']  # Isolate codes from DB_Seldon
    stacked_ticker_codes = pd.concat([eod_ticker_codes, db_ticker_codes], axis=0) # Create series of all codes
    missing_codes = stacked_ticker_codes.drop_duplicates(keep=False) # Drop all where duplicates leaving missing
    missing_tickers = ticker_data_eod[ticker_data_eod['Code'].isin(missing_codes)] # Filter out missing exchenges
    len_missing_tickers = len(missing_tickers)
    logging.debug(f"Missing DataFrames Identified")
    print(missing_tickers)
    print(len_missing_tickers)
    