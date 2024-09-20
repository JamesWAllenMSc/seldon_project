-- Reset static_data table
DROP TABLE api_call_count;

CREATE TABLE api_call_count
(
    Data_Type VARCHAR(50),
    Data_Values INTEGER(24)
)
    ENGINE = InnoDB
    Comment = 'Storage for static data to be called by app';

INSERT INTO api_call_count -- Confirm APIs remaining before deployment
    VALUES ('Daily APIs', 0),
            ('Extra APIs', 97071);


-- Reset global_exchanges table
DROP TABLE global_exchanges;

CREATE TABLE global_exchanges
(
    Name VARCHAR(50),
    Code VARCHAR(25),
    OperatingMIC VARCHAR(15),
    Country VARCHAR(50),
    Currency VARCHAR(15),
    CountryISO2 VARCHAR(15),
    CountryISO3 VARCHAR(15),
    Source VARCHAR(15),
    Date_Updated VARCHAR(50),
    PRIMARY KEY (Name)
)
    ENGINE = InnoDB
    Comment = 'Database of global exchanges';


-- Reset global_tickers table
DROP TABLE global_tickers;

CREATE TABLE global_tickers
(
    Ticker_ID VARCHAR(50),
    Code VARCHAR(50),
    Name VARCHAR(250),
    Country VARCHAR(15),
    Exchange VARCHAR(15),
    Currency VARCHAR(15),
    Type VARCHAR(15),
    Isin VARCHAR(15),
    Source VARCHAR(15),
    Date_Updated VARCHAR(50),
    PRIMARY KEY (Ticker_ID)
)
    ENGINE = InnoDB
    Comment = 'Database of global tickers';