import duckdb
import os


def download_parquet_files(months=None, output_dir='data/parquet'):
    """
    Download taxi parquet files from DuckDB data repository.
    
    Args:
        months: List of month numbers (e.g., ['04', '05', '06']). 
                Defaults to ['04', '05', '06']
        output_dir: Output directory path. Defaults to 'data/parquet'
    
    Returns:
        None
    """
    if months is None:
        months = ['04', '05', '06']
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Connect to DuckDB (in-memory database)
    conn = duckdb.connect()
    
    base_url = 'https://github.com/cwida/duckdb-data/releases/download/v1.0'
    
    for month in months:
        filename = f'taxi_2019_{month}.parquet'
        url = f'{base_url}/{filename}'
        output_path = os.path.join(output_dir, filename)
        
        # SQL command to download and save the parquet file
        sql = f"""
        COPY (
            SELECT * FROM READ_PARQUET('{url}')
        )
        TO '{output_path}' (FORMAT 'parquet');
        """
        
        try:
            # Execute the SQL command
            conn.execute(sql)
            print(f"Successfully downloaded {filename} to {output_dir}/")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
    
    # Close the connection
    conn.close()


if __name__ == '__main__':
    download_parquet_files()
