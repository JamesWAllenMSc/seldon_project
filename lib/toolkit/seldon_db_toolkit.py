from mysql.connector import connect
from mysql.connector import Error
import logging
import pandas as pd



def execute_query(access, query):
    """ Takes database access credentials and an sql query and executes
    the query in the specified database.
    -------------------------------------------------------------------
    
    Example code:

    import credentials
    import toolkit

    test_query = CREATE TABLE Persons (PersonID int, LastName varchar(255), FirstName varchar(255), Address varchar(255), City varchar(255));
    db_access = credentials.SeldonDBAppAccess()
    toolkit.execute_query(db_access, test_query)
    """
    
    try:
        with connect(
            host = access.db_host,
            user = access.db_user,
            password = access.db_password,
            database = access.db_database,           
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
            logging.debug(f"Execution complete for query: {query}")
            
    except Error as e:
        logging.error(e, exc_info=True)  


def retrieve_table(access, query):
    """ Takes access credentials and query and returns table as list of tuples
    --------------------------------------------------------------------------

    Example code:
    
    """

    try:
        with connect(
            host = access.db_host,
            user = access.db_user,
            password = access.db_password,
            database = access.db_database,           
        ) as connection:
            logging.debug("Connection to database succesful...")
            with connection.cursor() as cursor:
                cursor.execute(query)
                table = cursor.fetchall()
            logging.debug(f"Execution complete for query: {query}")
            return table
            
    except Error as e:
        logging.error(e, exc_info=True)

def update_api_count(access, apis_used):
    """ This function is used to keep track of the api calls by updating the table static_data
    """
    # Retrieve current API count
    retrieve_table_query = "SELECT * FROM api_call_count"
    api_call_count = retrieve_table(access, retrieve_table_query)
    api_call_count = pd.DataFrame(api_call_count)
    daily_apis = api_call_count.iloc[0,1]
    extra_apis = api_call_count.iloc[1,1]
    print(f'Daily APIs: {daily_apis}') # REMOVE AT DEPLOYMENT
    print(f'Extra APIs: {extra_apis}') # REMOVE AT DEPLOYMENT
    print(f'APIs Used: {apis_used}') # REMOVE AT DEPLOYMENT
    apis_remaining = extra_apis - apis_used
    print(f'Extra APIs Remaining: {apis_remaining}') # REMOVE AT DEPLOYMENT
    if apis_remaining <= 0:
        apis_used = abs(apis_remaining)
        print(f'APIs to be removed from daily apis: {apis_used}') # REMOVE AT DEPLOYMENT
        apis_remaining = 

    
    # daily_api_query = f'UPDATE static_data SET Data_Values = {daily_apis_remaining} WHERE Data_Values = "Daily APIs";'
    # extra_api_query = f'UPDATE static_data SET Data_Values = {extra_apis_remaining} WHERE Data_Values = "Extra APIs";'
    pass
