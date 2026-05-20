from pathlib import Path

import duckdb
import pandas as pd

DB_PATH = Path("data/processed/warehouse.duckdb")

MOBILITY_PATH = Path("../berlin-mobility-pipeline/data/processed/bike_counts_2025_clean.parquet")
WEATHER_PATH = Path("../berlin-weather-pipeline/data/processed/weather_2025_historical.parquet")


def load_mobility(con: duckdb.DuckDBPyConnection) -> None:
    """Load Berlin mobility data and create station, date, and fact tables."""
    df = pd.read_parquet(MOBILITY_PATH)

    df["date"] = pd.to_datetime(df["date"])
    df["date_id"] = df["date"].dt.strftime("%Y-%m-%d")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.weekday
    df["is_weekend"] = df["weekday"] >= 5

    con.execute("""
        CREATE OR REPLACE TABLE dim_station AS
        SELECT
            ROW_NUMBER() OVER () AS station_pk,
            station_id AS station_name
        FROM (
            SELECT DISTINCT station_id
            FROM df
        )
    """)

    con.execute("""
        CREATE OR REPLACE TABLE dim_date AS
        SELECT DISTINCT
            date_id,
            year,
            month,
            day,
            weekday,
            is_weekend
        FROM df
    """)

    con.execute("""
        CREATE OR REPLACE TABLE fact_bike_counts AS
        SELECT
            ROW_NUMBER() OVER () AS count_id,
            date_id,
            station_id AS station_name,
            bike_count,
            hour
        FROM df
    """)

    print(f"✅ Mobility loaded: {len(df)} rows")


def load_weather(con: duckdb.DuckDBPyConnection) -> None:
    """Load Berlin weather data and create the weather dimension table."""
    df = pd.read_parquet(WEATHER_PATH)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date_id"] = df["timestamp"].dt.strftime("%Y-%m-%d")

    con.execute("""
        CREATE OR REPLACE TABLE dim_weather AS
        SELECT
            ROW_NUMBER() OVER () AS weather_id,
            date_id,
            AVG(temperature_2m) AS avg_temp_c,
            SUM(precipitation) AS total_precipitation_mm,
            AVG(wind_speed_10m) AS avg_wind_speed
        FROM df
        GROUP BY date_id
    """)

    print(f"✅ Weather loaded: {len(df)} rows")


def main() -> None:
    """Build the local DuckDB analytics warehouse."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DB_PATH))

    try:
        load_mobility(con)
        load_weather(con)
        print("🎉 Warehouse built successfully!")
    finally:
        con.close()


if __name__ == "__main__":
    main()