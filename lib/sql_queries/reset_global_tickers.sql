DROP TABLE global_tickers;

CREATE TABLE global_tickers
(
    Ticker_ID VARCHAR(25),
    Code VARCHAR(15),
    Name VARCHAR(150),
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