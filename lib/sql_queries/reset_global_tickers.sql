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
    Comment = 'Database of global tickers'