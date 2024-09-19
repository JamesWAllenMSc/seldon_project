"""This function retrieves the exchanges list held on seldon_db and
compares it to the list of exchanges held on EodHD.com. Any that are
missing are added to the database.
"""


import toolkit
import credentials as access
import logging
import pandas as pd
import numpy as np


def exchanges_update():
    apis_remaining = toolkit.retrieve_api_count
    while apis_remaining > 0:
        try:
            # RETRIEVE EXCHANGE DATA FROM SERVER
            retrieve_table_query = 'SELECT * FROM global_exchanges;'

            # Declare columns for database
            db_columns = ['Name', 'Code', 'OperatingMIC', 'Country',
                        'Currency', 'CountryISO2', 'CountryISO3', 'Source', 
                        'Date_Updated']
            # Run query retrieving database with declared column names
            db_exchange_data = toolkit.retrieve_table(access, retrieve_table_query)
            db_exchange_data = pd.DataFrame(db_exchange_data, columns=db_columns)
            logging.debug(f"Data retrieved from seldon_db and processed")

            # RETRIEVE EXCHANGE LIST FROM EOD.COM
            eod_exchange_data = toolkit.retrieve_exchanges(access, access.eodhd_api)
            apis_remaining = apis_remaining - 1
            # Drop unused exchenges
            exchanges_drop_list = ['MONEY', 'BRVM']
            for exchange in exchanges_drop_list:
                    index_to_drop = eod_exchange_data[eod_exchange_data['Code'] == exchange].index
                    eod_exchange_data = eod_exchange_data.drop(index_to_drop)
            logging.debug(f"Data retrieved from EoDHD.com")

            # CHECK THERE ARE NO CHANGES TO HEADERS
            logging.debug("Checking header changes")
            headers_eod = eod_exchange_data.columns.values
            db_col_array = np.array(db_columns)
            if np.array_equal(headers_eod, db_col_array):
                logging.debug(f"EodHD / Seldon_DB Exchanges column check: COMPLETE")
            else:
                logging.error(f"EodHD / Seldon_DB Exchanges column check: FAILED")
                exit

            # FILTER EXCHANGES MISSING FROM SELDON_DB
            eod_exchange_codes = eod_exchange_data['Code'] # Isolate codes from EoDHD.com
            db_exchange_codes = db_exchange_data['Code']  # Isolate codes from DB_Seldon
            stacked_codes = pd.concat([eod_exchange_codes, db_exchange_codes], axis=0) # Create series of all codes
            missing_codes = stacked_codes.drop_duplicates(keep=False) # Drop all where duplicates leaving missing
            missing_exchanges = eod_exchange_data[eod_exchange_data['Code'].isin(missing_codes)] # Filter out missing exchenges
            len_missing_exchanges = len(missing_exchanges)
            logging.debug(f"Missing DataFrames Identified")
            
            if len_missing_exchanges > 0:
                # PREPARE MISSING EXCHANGES FOR UPLOAD TO SELDON_DB
                missing_exchanges_columns = missing_exchanges.columns.values
                columns = ', '.join(missing_exchanges_columns) # Columns prepped 
                missing_exchanges = missing_exchanges.replace({np.nan:'None'})
                missing_exchanges = str(missing_exchanges.values.tolist())
                missing_exchanges = missing_exchanges.replace('[', '(').replace(']', ')')
                missing_exchanges = missing_exchanges[1:-1]

                # ADD EXCHANGES TO SELDON_DB
                add_record_query = f'INSERT INTO global_exchanges ({columns}) VALUES {missing_exchanges};'
                toolkit.execute_query(access, add_record_query)
                logging.info(f"Exchanges checked, {len_missing_exchanges} exchanges added to seldon_db")
            else:
                logging.info(f"Exchanges checked, no new exchanges detected")
            toolkit.update_api_count(access, apis_remaining)
        except Exception as e:
                    logging.error(e, exc_info=True)
    else:
         logging.info(f"Ran out of API calls while executing exchanges_update.py")
         

