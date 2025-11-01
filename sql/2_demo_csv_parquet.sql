-- csv_parquet_demo.sql
-- This script demonstrates reading from Parquet files, creating tables,
-- converting to CSV, and working with Parquet format.

-- 1. Preview data from our existing Parquet file
SELECT * FROM read_parquet('data/parquet/taxi_2019_04.parquet') LIMIT 3;

-- 2. Show tables (if any exist)
SHOW tables;

-- 3. Create a table from our Parquet file
CREATE TABLE taxi_trips AS 
SELECT * FROM read_parquet('data/parquet/taxi_2019_04.parquet');

-- 4. Show tables to confirm creation
SHOW tables;

-- 5. Export the table to CSV format
COPY taxi_trips TO 'data/csv/taxi_2019_04.csv' (HEADER, DELIMITER ',');

-- 6. Export the table to a new Parquet file
COPY taxi_trips TO 'data/parquet/taxi_2019_04_exported.parquet' (FORMAT PARQUET);

-- 7. Read from the exported Parquet file to verify
SELECT * FROM read_parquet('data/parquet/taxi_2019_04_exported.parquet') LIMIT 5;
