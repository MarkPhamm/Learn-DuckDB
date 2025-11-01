"""
Convert Parquet files to CSV format using DuckDB.
"""
import duckdb
from pathlib import Path


def convert_parquet_to_csv(input_dir: str = "data/parquet", output_dir: str = "data/csv"):
    """
    Convert all Parquet files in the input directory to CSV files in the output directory.

    Args:
        input_dir: Directory containing the Parquet files (default: "data/parquet")
        output_dir: Directory where CSV files will be written (default: "data/csv")
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        return

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all parquet files
    parquet_files = list(input_path.glob("*.parquet"))

    if not parquet_files:
        print(f"No Parquet files found in '{input_dir}'")
        return

    print(f"Found {len(parquet_files)} Parquet file(s)")

    # Create DuckDB connection
    con = duckdb.connect()

    for parquet_file in parquet_files:
        csv_file = output_path / parquet_file.with_suffix(".csv").name

        print(f"Converting {parquet_file.name} -> {csv_file.name}...", end=" ")

        try:
            # Use DuckDB to read Parquet and write to CSV
            con.execute(f"""
                COPY (SELECT * FROM read_parquet('{parquet_file}'))
                TO '{csv_file}'
                (HEADER, DELIMITER ',')
            """)
            print("Done")
        except Exception as e:
            print(f"Error: {e}")

    con.close()
    print("\nConversion complete!")


if __name__ == "__main__":
    convert_parquet_to_csv()
