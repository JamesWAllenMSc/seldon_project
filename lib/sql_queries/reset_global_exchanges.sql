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
    Comment = 'Database of global exchanges'