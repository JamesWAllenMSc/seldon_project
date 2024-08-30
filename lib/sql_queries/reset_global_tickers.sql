DROP TABLE global_tickers;

CREATE TABLE global_tickers
(
    Code VARCHAR(15),
    Name VARCHAR(50),
    Country VARCHAR(15),
    Exchange VARCHAR(15),
    Currency VARCHAR(15),
    Type VARCHAR(15),
    Isin VARCHAR(15),
    Source VARCHAR(15),
    Date_Updated VARCHAR(50),
    PRIMARY KEY (Code)
)
    ENGINE = InnoDB
    Comment = 'Database of global tickers'