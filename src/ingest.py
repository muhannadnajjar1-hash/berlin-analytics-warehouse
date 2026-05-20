import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = "data/processed/warehouse.duckdb"

MOBILITY_PATH = "../berlin-mobility-pipeline/data/processed/bike_counts_2025_clean.parquet"
WEATHER_PATH  = "../berlin-weather-pipeline/data/processed/weather_2025_historical.parquet"

def load_mobility(con):
    df = pd.read_parquet(MOBILITY_PATH)
    df["date_id"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["year"]       = pd.to_datetime(df["date"]).dt.year
    df["month"]      = pd.to_datetime(df["date"]).dt.month
    df["day"]        = pd.to_datetime(df["date"]).dt.day
    df["is_weekend"] = pd.to_datetime(df["date"]).dt.weekday >= 5

    # dim_station
    stations = df[["station_id"]].drop_duplicates().reset_index(drop=True)
    stations["station_id_int"] = range(1, len(stations) + 1)
    con.execute("""
        CREATE TABLE IF NOT EXISTS dim_station AS
        SELECT ROW_NUMBER() OVER () AS station_pk, station_id AS station_name
        FROM (SELECT DISTINCT station_id FROM df)
    """)

    # dim_date
    con.execute("""
        CREATE TABLE IF NOT EXISTS dim_date AS
        SELECT DISTINCT date_id, year, month, day, weekday, is_weekend FROM df
    """)

    # fact_bike_counts
    con.execute("""
        CREATE TABLE IF NOT EXISTS fact_bike_counts AS
        SELECT
            ROW_NUMBER() OVER () AS count_id,
            date_id,
            station_id AS station_name,
            bike_count,
            hour
        FROM df
    """)
    print(f"✅ Mobility loaded: {len(df)} rows")

def load_weather(con):
    df = pd.read_parquet(WEATHER_PATH)
    df["date_id"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d")

    con.execute("""
        CREATE TABLE IF NOT EXISTS dim_weather AS
        SELECT
            ROW_NUMBER() OVER () AS weather_id,
            date_id,
            AVG(temperature_2m)  AS avg_temp_c,
            SUM(precipitation)   AS total_precipitation_mm,
            AVG(wind_speed_10m)  AS avg_wind_speed
        FROM df
        GROUP BY date_id
    """)
    print(f"✅ Weather loaded: {len(df)} rows")

if __name__ == "__main__":
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(DB_PATH)
    load_mobility(con)
    load_weather(con)
    print("🎉 Warehouse built successfully!")
    con.close()
