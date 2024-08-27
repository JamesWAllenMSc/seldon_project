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
        logging.error(e)


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
        logging.error(e)