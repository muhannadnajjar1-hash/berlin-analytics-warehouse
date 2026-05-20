-- Analysis queries for the Berlin Analytics Warehouse.
-- These queries are designed to run after building data/processed/warehouse.duckdb.

-- 1. Total bike counts per day
SELECT
    date_id,
    SUM(bike_count) AS total_bikes
FROM fact_bike_counts
GROUP BY date_id
ORDER BY date_id;

-- 2. Top 10 busiest stations
SELECT
    station_name,
    SUM(bike_count) AS total_bikes
FROM fact_bike_counts
GROUP BY station_name
ORDER BY total_bikes DESC
LIMIT 10;

-- 3. Weekday vs weekend traffic
SELECT
    d.is_weekend,
    AVG(f.bike_count) AS avg_bikes
FROM fact_bike_counts AS f
JOIN dim_date AS d
    ON f.date_id = d.date_id
GROUP BY d.is_weekend
ORDER BY d.is_weekend;

-- 4. Busiest hours of the day
SELECT
    hour,
    AVG(bike_count) AS avg_bikes
FROM fact_bike_counts
GROUP BY hour
ORDER BY hour;

-- 5. Bike traffic by weather type
-- This query connects mobility data with weather data using date_id.
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
ORDER BY weather_type;

-- 6. Monthly bike traffic trend
SELECT
    d.month,
    SUM(f.bike_count) AS total_bikes
FROM fact_bike_counts AS f
JOIN dim_date AS d
    ON f.date_id = d.date_id
GROUP BY d.month
ORDER BY d.month;

-- 7. Daily bike traffic with weather metrics
-- This is the main query that proves the connection between
-- Berlin Mobility Pipeline and Berlin Weather Pipeline.
SELECT
    f.date_id,
    SUM(f.bike_count) AS total_bike_count,
    ROUND(AVG(w.avg_temp_c), 2) AS avg_temp_c,
    ROUND(AVG(w.total_precipitation_mm), 2) AS total_precipitation_mm,
    ROUND(AVG(w.avg_wind_speed), 2) AS avg_wind_speed
FROM fact_bike_counts AS f
JOIN dim_weather AS w
    ON f.date_id = w.date_id
GROUP BY f.date_id
ORDER BY f.date_id;