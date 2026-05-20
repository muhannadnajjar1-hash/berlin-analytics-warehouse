-- Schema reference for the Berlin Analytics Warehouse.
-- These tables are created by src/ingest.py in DuckDB.

-- Dimension: Station
CREATE OR REPLACE TABLE dim_station AS
SELECT
    ROW_NUMBER() OVER () AS station_pk,
    station_id AS station_name
FROM (
    SELECT DISTINCT station_id
    FROM df
);

-- Dimension: Date
CREATE OR REPLACE TABLE dim_date AS
SELECT DISTINCT
    date_id,
    year,
    month,
    day,
    weekday,
    is_weekend
FROM df;

-- Dimension: Weather
CREATE OR REPLACE TABLE dim_weather AS
SELECT
    ROW_NUMBER() OVER () AS weather_id,
    date_id,
    AVG(temperature_2m) AS avg_temp_c,
    SUM(precipitation) AS total_precipitation_mm,
    AVG(wind_speed_10m) AS avg_wind_speed
FROM df
GROUP BY date_id;

-- Fact: Bike Counts
CREATE OR REPLACE TABLE fact_bike_counts AS
SELECT
    ROW_NUMBER() OVER () AS count_id,
    date_id,
    station_id AS station_name,
    bike_count,
    hour
FROM df;