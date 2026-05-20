-- 1. Total bike counts per day
SELECT date_id, SUM(bike_count) AS total_bikes
FROM fact_bike_counts
GROUP BY date_id
ORDER BY date_id;

-- 2. Top 10 busiest stations
SELECT station_name, SUM(bike_count) AS total_bikes
FROM fact_bike_counts
GROUP BY station_name
ORDER BY total_bikes DESC
LIMIT 10;

-- 3. Weekday vs Weekend traffic
SELECT is_weekend, AVG(bike_count) AS avg_bikes
FROM fact_bike_counts f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY is_weekend;

-- 4. Busiest hours of the day
SELECT hour, AVG(bike_count) AS avg_bikes
FROM fact_bike_counts
GROUP BY hour
ORDER BY hour;

-- 5. Rain vs bike traffic correlation
SELECT
    CASE WHEN w.total_precipitation_mm > 1 THEN 'Rainy' ELSE 'Dry' END AS weather_type,
    AVG(f.bike_count) AS avg_bikes
FROM fact_bike_counts f
JOIN dim_weather w ON f.date_id = w.date_id
GROUP BY weather_type;

-- 6. Monthly trend
SELECT d.month, SUM(f.bike_count) AS total_bikes
FROM fact_bike_counts f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.month
ORDER BY d.month;
