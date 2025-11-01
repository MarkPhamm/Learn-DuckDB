# Learn-DuckDB

## What's DuckDB

DuckDB is an in-process SQL OLAP database, which means it runs within the same process as the application using it. This unique feature allows DuckDB to offer the advantages of a database without the complexities of managing one.

The reason why I love DuckDB is that it's the easiest OLAP database you can set up. You don't need no Snowflake free tier or stomp your foot into the AWS redshift free tier trap. It's simple, a `.db` file inside of your computer :) However, it's noted to mention that duckdb is a **in-memory** process, by default, it won't persist any data. But don't worry, there's a work around for this using `.open`

Also, instead of writing transformation logic in Python (Pandas) of which I'm not really good at, I can now write custom transformation logic with SQL, of which I'm wayyyyy more confident with.

## 1. Set up

### 1.1 Installing DuckDB's cli

```zsh
brew install duckdb
```

### 1.2 Creating a Virtual Environment

A virtual environment (venv) is an isolated Python environment that allows you to install packages and dependencies specific to a project without affecting your system-wide Python installation. This isolation ensures that different projects can have different versions of the same package, preventing conflicts and making your development environment more reproducible and manageable.

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1.3 Prepare the directories

The dataset files are large, so you'll need to manually download the Parquet files and place them in the data directory.

```zsh
mkdir data
cd data

mkdir parquet
mkdir csv
```

After creating the data directory, we will create 2 subfolder csv and parquet accordingly. After that copy all of the parquet files into the data directory.

## 3. A bit about Parquet Files

Parquet is a columnar storage file format optimized for use with big data processing frameworks. Unlike row-based formats (like CSV), Parquet stores data by column, which makes it highly efficient for analytical queries that only need to read specific columns. Key benefits include:

- **Compression**: Parquet files are highly compressed, reducing storage costs and improving I/O performance
- **Schema preservation**: The file format stores the data schema, including column names and types
- **Efficient querying**: Columnar storage allows for faster aggregations and filtering operations
- **Cross-platform**: Parquet is supported by many data processing tools including DuckDB, Pandas, Polars, and Apache Spark

DuckDB can read Parquet files directly without loading them entirely into memory, making it ideal for analyzing large datasets.

### 3.1 Set up, download the parquet files

Previously, downloading Parquet files was a manual process. However, we've automated this task using DuckDB's ability to read Parquet files directly from remote URLs. This approach leverages DuckDB's native HTTP/HTTPS support, allowing us to download files efficiently without needing additional HTTP libraries.

The project includes a Python script (`src/download_parquet.py`) that uses DuckDB's `READ_PARQUET()` function to fetch Parquet files from the DuckDB data repository and saves them locally. The script automatically downloads three taxi trip data files for April, May, and June 2019.

To download the Parquet files:

```zsh
python src/download_parquet.py
```

The script will:

- Create the `data/parquet` directory if it doesn't exist
- Download `taxi_2019_04.parquet`, `taxi_2019_05.parquet`, and `taxi_2019_06.parquet` from the DuckDB data repository
- Save all files to the `data/parquet` directory

You can also customize the script to download different months by modifying the function call:

```python
from src.download_parquet import download_parquet_files

# Download specific months
download_parquet_files(months=['04', '05', '06', '07'])
```

This automated approach is much more convenient than manual downloads and demonstrates one of DuckDB's powerful features: its ability to work with remote data sources seamlessly.

### 3.2 Convert parquet file to CSVs

To demonstrate the efficiency of Parquet files compared to CSV format, we'll convert the Parquet files to CSV format using DuckDB. This conversion allows us to compare file sizes and understand the storage benefits of Parquet.

The project includes a Python script (`src/parquet_to_csv.py`) that leverages DuckDB's ability to read Parquet files directly and export them as CSV. The script automatically processes all Parquet files in the `data/parquet` directory and converts them to corresponding CSV files in the `data/csv` directory.

To run the conversion:

```zsh
python src/parquet_to_csv.py
```

The script uses DuckDB's `read_parquet()` function to read the Parquet files and `COPY ... TO` command to export the data to CSV format with headers. This approach is efficient because DuckDB can process the Parquet files column-by-column without loading the entire dataset into memory.

### 3.2 Evaluate the results

Let's take a look at what happen when we convert the parquet file into csv files. Let's cd into `data/csv` dir and `data\parquet` dir respectively

```zsh
cd data/parquet
ls -la

cd ..

cd data/csv
ls -la
```

### Example output

Parquet output

```zsh
.rw-r--r--@ 127M user_name 31 Oct 21:32 taxi_2019_04.parquet
.rw-r--r--@ 130M user_name 31 Oct 21:32 taxi_2019_05.parquet
.rw-r--r--@ 121M user_name 31 Oct 21:32 taxi_2019_06.parquet
```

csv output

```zsh
.rw-r--r--@ 718M user_name 31 Oct 21:48 taxi_2019_04.csv
.rw-r--r--@ 731M user_name 31 Oct 21:48 taxi_2019_05.csv
.rw-r--r--@ 671M user_name 31 Oct 21:48 taxi_2019_06.csv
```

Wow! We can see that parquet file size are about 6-7 times smaller than CSVs file. This dramatic reduction in file size not only saves storage space but also significantly improves query performance, as less data needs to be read from disk. For large-scale data analysis, using Parquet format can make a substantial difference in both cost and performance.

This is one of the key reasons why DuckDB is optimized to work with Parquet files—you get the benefits of columnar storage and compression while maintaining the ability to query your data using standard SQL syntax.

### 3.3 Delete CSVs

Now that we've demonstrated the significant size difference between Parquet and CSV files, we can clean up by deleting the CSV files to save disk space. Since DuckDB can read Parquet files directly, we don't need the CSV files for our analysis.

```zsh
cd data/csv
rm *.csv
```

Or if you want to remove the entire csv directory:

```zsh
cd data
rm -rf csv
```

This frees up approximately 2GB of disk space while keeping the original Parquet files that are much more efficient for querying with DuckDB.

## 4. Working with DuckDB

Now that we understand the advantages of Parquet files, let's explore how to use DuckDB to query our taxi trip data. DuckDB can read Parquet files directly without importing them into a database, making it perfect for analyzing large datasets efficiently.

## 4.1 Understanding DuckDB Architecture

DuckDB is an embedded analytical SQL database designed for in-process analytics.
Unlike traditional client-server databases, DuckDB runs directly inside applications, sharing the same process and memory space. This design makes it lightweight, fast, and easy to integrate into Python, R, or other host environments.

### 4.2 Key Architectural Features

- **In-Process Execution**
  DuckDB operates within the host process, eliminating network overhead and improving performance for analytical workloads.

- **Columnar Storage**
  Data is stored column-wise, enabling faster analytical queries since only the required columns are read into memory.

- **Vectorized Execution Engine**
  Queries are executed in vectorized batches, optimizing CPU cache usage and accelerating large-scale computations.

- **ACID Compliance**
  Despite its lightweight nature, DuckDB supports transactional guarantees (Atomicity, Consistency, Isolation, Durability).

- **Cross-Language Support**
  DuckDB provides bindings for multiple languages, including Python, R, and C++, and can directly query Parquet, CSV, and Arrow data formats.

- **Self-Contained Design**
  It requires no external dependencies or server setup—everything is contained in a single library file.

---

## 4.3 DuckDB’s Example Use Case

DuckDB is often used for fast, local data analysis where users want SQL power without the overhead of a database server.
A typical use case is querying large CSV or Parquet files directly from Python.

### Example

```python
import duckdb

query = """
SELECT category, SUM(sales) AS total_sales
FROM 'data/sales.csv'
GROUP BY category
ORDER BY total_sales DESC
"""

result = duckdb.query(query).to_df()
print(result.head())
```

### 4.4 Running SQL file with DuckDB's CLI

DuckDB provides a command-line interface (CLI) that allows you to execute SQL commands interactively or run SQL scripts from files. This is particularly useful for batch processing, testing queries, or automating data workflows.

**From the command line (outside DuckDB CLI):**

To run a SQL file using DuckDB's CLI, you can use input redirection:

```zsh
duckdb < sql/demo.sql
```

Or initialize DuckDB with a SQL file:

```zsh
duckdb -init sql/demo.sql
```

**From inside DuckDB CLI (interactive mode):**

If you're already inside the DuckDB CLI (you'll see the `D` prompt), you can't use shell redirection. Instead, use the `.read` command to execute a SQL file:

```zsh
# Start DuckDB CLI
duckdb

# Inside DuckDB CLI, run:
.read sql/demo.sql
```

**Note:** When inside the DuckDB CLI, shell commands like `duckdb < file.sql` won't work. Use `.read` instead.

### 4.5 Persisting Data in DuckDB

By default, DuckDB runs in **in-memory mode**, which means all data is stored in RAM and will be lost when the connection is closed. However, DuckDB can also persist data to disk by connecting to a database file (`.db` file).

#### Why Persist Data?

While in-memory mode is great for quick analysis and testing, you'll want to persist data when:

- You need to keep data between sessions
- Working with large datasets that should be stored on disk
- Building a data pipeline that needs to maintain state
- Sharing data across multiple sessions or applications

#### Using a Persistent Database File

**With DuckDB CLI:**

To connect to a persistent database file (or create one if it doesn't exist):

```zsh
# Connect to a database file
duckdb database/my_database.db

# Run SQL file against a persistent database
duckdb database/my_database.db < sql/demo.sql

# or use the open command
duckdb 


```

**With Python:**

```python
import duckdb

# Connect to a persistent database file
conn = duckdb.connect('database/my_database.db')

# All tables and data created will persist to this file
conn.execute("CREATE TABLE ducks AS SELECT 3 AS age, 'mandarin' AS breed")
conn.execute("SHOW tables")

# Close connection - data is saved to disk
conn.close()

# Reconnect later - your data is still there!
conn = duckdb.connect('database/my_database.db')
result = conn.execute("SELECT * FROM ducks").fetchall()
print(result)
```

#### In-Memory vs Persistent Database

| Feature | In-Memory (`duckdb.connect()`) | Persistent (`duckdb.connect('file.db')`) |
|--------|-------------------------------|------------------------------------------|
| Storage | RAM only | Disk file (.db) |
| Persistence | Data lost on disconnect | Data persists after disconnect |
| Speed | Faster (RAM access) | Slightly slower (disk I/O) |
| Use Case | Quick analysis, testing | Production data, long-term storage |

#### Example: Creating and Querying a Persistent Database

```python
import duckdb

# Create/connect to persistent database
conn = duckdb.connect('database/taxi_data.db')

# Create a table from a Parquet file
conn.execute("""
    CREATE TABLE taxi_trips AS 
    SELECT * FROM read_parquet('data/parquet/taxi_2019_04.parquet')
""")

# Query the persistent data
result = conn.execute("""
    SELECT 
        COUNT(*) as total_trips,
        AVG(fare_amount) as avg_fare
    FROM taxi_trips
""").fetchall()

print(result)

# Close - data is saved to database/taxi_data.db
conn.close()
```

The database file will be created in the `database/` directory and will contain all your tables and data, ready to use in future sessions.

## 5. MotherDuck

MotherDuck is a cloud service built on top of DuckDB.
It extends DuckDB’s capabilities by offering a hybrid model where queries can be executed either locally or in the cloud. This allows users to handle both small local datasets and large-scale cloud data with the same SQL interface.

### 5.1 Core Concepts

- **Hybrid Query Execution**: Queries can run locally within DuckDB or offloaded to the cloud for scaling larger datasets.

- **Shared Instance**: MotherDuck manages DuckDB instances in the cloud, allowing persistent data storage and collaborative access across users.

- **Duckling**: “Ducklings” are lightweight, serverless instances of DuckDB used by MotherDuck to execute queries efficiently without needing manual provisioning.

- **Unified Experience**: Users can connect to local or remote data seamlessly using the same DuckDB syntax and client tools.

- **Integration Support**: MotherDuck supports direct connections to S3, BigQuery, and Parquet files, making it suitable for hybrid data environments.

## 5.2 Comparison: MotherDuck vs Other Cloud Data Warehouses

| Feature          | MotherDuck                                     | BigQuery                   | Snowflake                  | Redshift               |
| ---------------- | ---------------------------------------------- | -------------------------- | -------------------------- | ---------------------- |
| Base Engine      | DuckDB                                         | Proprietary                | Proprietary                | PostgreSQL-based       |
| Model            | Hybrid (local + cloud)                         | Fully cloud                | Fully cloud                | Fully cloud            |
| Scale            | Medium (elastic with Ducklings)                | Very large                 | Very large                 | Large                  |
| Setup            | Minimal, no infrastructure                     | Managed setup              | Managed setup              | Requires configuration |
| Cost             | Pay-per-usage, efficient for smaller workloads | Pay-per-query              | Credit-based               | Usage/hourly           |
| Ideal For        | Developers, analysts, small teams              | Enterprise-scale analytics | Enterprise-scale analytics | AWS-based enterprises  |
| Open Source Core | Yes (DuckDB)                                   | No                         | No                         | No                     |

MotherDuck combines DuckDB’s lightweight nature with cloud scalability, offering a simple alternative to heavy enterprise data warehouses.

## 5.3 Advantages and Limitations of MotherDuck

### Advantages

- Simple setup with no infrastructure management.
- Hybrid compute (local + cloud) offers flexibility.
- Cost-effective for analytical workloads of small to medium scale.
- Based on DuckDB, allowing familiar local workflows.
- “Ducklings” enable efficient scaling without full server provisioning.

### Limitations

- Not optimized for very large, distributed workloads like petabyte-scale systems.
- Limited to analytical use cases; not suited for OLTP operations.
- Still maturing compared to long-established platforms like BigQuery or Snowflake.
