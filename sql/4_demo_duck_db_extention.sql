SELECT * FROM duckdb_extensions();
INSTALL httpfs;
LOAD httpfs;

-- Use raw.githubusercontent.com instead of github.com/blob for direct file access
CREATE TABLE bike AS SELECT * FROM read_parquet('https://raw.githubusercontent.com/MarkPhamm/perpay-bike-share-challenge/main/data/parquet/indego-trips-2020-q1.parquet');

-- Show table schema
DESCRIBE bike;

-- Preview the data
SELECT * FROM bike LIMIT 5;
