"""This script takes the exchanges from seldon_db and iterates over the exchange codes updating 
the list of tickers held on the database. 
"""

import toolkit
import credentials as access
import logging
import toolkit
import pandas as pd
import numpy as np


def ticker_update():
    # GET EXCHANGES LIST FROM SELDON_DB
    table_query = 'SELECT Code FROM global_exchanges;'
    col_name = ['Code']
    table = toolkit.retrieve_table(access, table_query)
    table = pd.DataFrame(table, columns=col_name)
    exchange_list = table['Code'].to_list()
    logging.debug(f"Exchanges retrieved from seldon_db.global_exchanges")
    # ITERATE OVER EXCHANGES LIST RETRIEVING TICKERS FOR EACH EXCHANGE 
    # ON BOTH SELDON_DB AND EODHD.COM
    total_tickers = 0 # Start count of tickers for logging
    try:
        for exchange_code in exchange_list:
            # Request ticker list from seldon_db filtered by exchange code
            exchange_code_prepped = f"'{exchange_code}'"
            table_query = f'SELECT * FROM global_tickers WHERE Exchange={exchange_code_prepped};'
            db_columns = ['Ticker_ID', 'Code', 'Name', 'Country', 'Exchange',
                        'Currency', 'Type', 'Isin', 'Source',
                        'Date_Updated']
            table = toolkit.retrieve_table(access, table_query) # ISSUE
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
            logging.debug(f"{len_missing_tickers} missing tickers Identified")
            
            # IF NEW TICKERS ARE IDENTIFIED ADD THEM
            if len_missing_tickers > 0:
                # PREPARE MISSING EXCHANGES FOR UPLOAD TO SELDON_DB
                missing_tickers_columns = missing_tickers.columns.values
                columns = ', '.join(missing_tickers_columns) # Columns prepped
                missing_tickers = missing_tickers.replace({np.nan:'None'})
                missing_tickers = str(missing_tickers.values.tolist())
                missing_tickers = missing_tickers.replace('[', '(').replace(']', ')')
                missing_tickers = missing_tickers[1:-1]
                # ADD EXCHANGES TO SELDON_DB
                add_record_query = f'INSERT INTO global_tickers ({columns}) VALUES {missing_tickers};'
                toolkit.execute_query(access, add_record_query)
                total_tickers = total_tickers + len_missing_tickers
            else:
                pass
                
        if total_tickers > 0:
            logging.info(f"Exchanges checked, {total_tickers} tickers added to seldon_db")
        else:
            logging.info(f"Tickers checked, no new tickers detected")
    except Exception as e:
        logging.error(e, exc_info=True)

# ticker_update()