from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import pandas as pd

DB_PATH = Path("data/processed/warehouse.duckdb")
FIGURES_DIR = Path("Reports/figures")


def save_top_stations(con: duckdb.DuckDBPyConnection) -> None:
    query = """
        SELECT
            station_name,
            SUM(bike_count) AS total_bikes
        FROM fact_bike_counts
        GROUP BY station_name
        ORDER BY total_bikes DESC
        LIMIT 10
    """
    df = con.execute(query).df()

    plt.figure(figsize=(10, 6))
    plt.barh(df["station_name"], df["total_bikes"])
    plt.title("Top 10 Bike Counting Stations")
    plt.xlabel("Total bike count")
    plt.ylabel("Station")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "top_stations.png", dpi=300)
    plt.close()


def save_monthly_trend(con: duckdb.DuckDBPyConnection) -> None:
    query = """
        SELECT
            d.month,
            SUM(f.bike_count) AS total_bikes
        FROM fact_bike_counts AS f
        JOIN dim_date AS d
            ON f.date_id = d.date_id
        GROUP BY d.month
        ORDER BY d.month
    """
    df = con.execute(query).df()

    plt.figure(figsize=(10, 5))
    plt.plot(df["month"], df["total_bikes"], marker="o")
    plt.title("Monthly Bike Traffic Trend")
    plt.xlabel("Month")
    plt.ylabel("Total bike count")
    plt.xticks(df["month"])
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "monthly_trend.png", dpi=300)
    plt.close()


def save_hourly_pattern(con: duckdb.DuckDBPyConnection) -> None:
    query = """
        SELECT
            hour,
            AVG(bike_count) AS avg_bikes
        FROM fact_bike_counts
        GROUP BY hour
        ORDER BY hour
    """
    df = con.execute(query).df()

    plt.figure(figsize=(10, 5))
    plt.plot(df["hour"], df["avg_bikes"], marker="o")
    plt.title("Average Bike Traffic by Hour")
    plt.xlabel("Hour of day")
    plt.ylabel("Average bike count")
    plt.xticks(df["hour"])
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "hourly_pattern.png", dpi=300)
    plt.close()


def save_rain_vs_dry(con: duckdb.DuckDBPyConnection) -> None:
    query = """
        SELECT
            CASE
                WHEN w.total_precipitation_mm > 1 THEN 'Rainy'
                ELSE 'Dry'
            END AS weather_type,
            AVG(f.bike_count) AS avg_bikes
        FROM fact_bike_counts AS f
        JOIN dim_weather AS w
            ON f.date_id = w.date_id
        GROUP BY weather_type
        ORDER BY weather_type
    """
    df = con.execute(query).df()

    plt.figure(figsize=(7, 5))
    plt.bar(df["weather_type"], df["avg_bikes"])
    plt.title("Average Bike Traffic: Rainy vs Dry Days")
    plt.xlabel("Weather type")
    plt.ylabel("Average bike count")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "rain_vs_dry.png", dpi=300)
    plt.close()


def save_daily_bike_traffic_vs_temperature(con: duckdb.DuckDBPyConnection) -> None:
    query = """
        SELECT
            f.date_id,
            SUM(f.bike_count) AS total_bike_count,
            AVG(w.avg_temp_c) AS avg_temp_c
        FROM fact_bike_counts AS f
        JOIN dim_weather AS w
            ON f.date_id = w.date_id
        GROUP BY f.date_id
        ORDER BY f.date_id
    """
    df = con.execute(query).df()
    df["date_id"] = pd.to_datetime(df["date_id"])

    plt.figure(figsize=(11, 6))
    plt.scatter(df["avg_temp_c"], df["total_bike_count"])
    plt.title("Daily Bike Traffic vs Average Temperature")
    plt.xlabel("Average temperature (°C)")
    plt.ylabel("Total daily bike count")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "daily_bike_traffic_vs_temperature.png", dpi=300)
    plt.close()


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"{DB_PATH} does not exist. Run `python3 src/ingest.py` first."
        )

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DB_PATH))

    try:
        save_top_stations(con)
        save_monthly_trend(con)
        save_hourly_pattern(con)
        save_rain_vs_dry(con)
        save_daily_bike_traffic_vs_temperature(con)
    finally:
        con.close()

    print(f"Reports saved to {FIGURES_DIR}")


if __name__ == "__main__":
    main()