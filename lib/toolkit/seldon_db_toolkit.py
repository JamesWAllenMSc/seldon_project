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
    apis_remaining = daily_apis - apis_used
    
    
    if apis_remaining <= 0:
        daily_apis_remaining = 0 
        apis_used = abs(apis_remaining)
        extra_apis_remaining = extra_apis - apis_used
    
    elif apis_remaining > 0:
        daily_apis_remaining = apis_remaining
        extra_apis_remaining = extra_apis
    
    extra_api_query = f'UPDATE api_call_count SET Data_Values = {extra_apis_remaining} WHERE Data_Type = "Extra APIs";'
    daily_api_query = f'UPDATE api_call_count SET Data_Values = {daily_apis_remaining} WHERE Data_Type = "Daily APIs";'
    execute_query(access, extra_api_query)
    execute_query(access, daily_api_query)


def retrieve_api_count(access):
    query = "SELECT * FROM api_call_count"
    api_call_count = retrieve_table(access, query)
    api_call_count = pd.DataFrame(api_call_count)
    daily_apis = api_call_count.iloc[0,1]
    extra_apis = api_call_count.iloc[1,1]
    total_apis = daily_apis + extra_apis
    return(total_apis)

    
