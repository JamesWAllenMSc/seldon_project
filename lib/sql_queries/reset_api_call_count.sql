-- Reset static_data table
DROP TABLE api_call_count;

CREATE TABLE api_call_count
(
    Data_Type VARCHAR(50),
    Data_Values FLOAT(24)
)
    ENGINE = InnoDB
    Comment = 'Storage for static data to be called by app';

INSERT INTO api_call_count -- Confirm APIs remaining before deployment
    VALUES ('Daily APIs', 100000),
            ('Extra APIs', 97593);