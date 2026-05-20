-- Dimension: Station
CREATE TABLE IF NOT EXISTS dim_station (
    station_id   INTEGER PRIMARY KEY,
    station_name TEXT NOT NULL,
    location     TEXT
);

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_id    TEXT PRIMARY KEY,  -- format: YYYY-MM-DD
    year       INTEGER,
    month      INTEGER,
    day        INTEGER,
    weekday    TEXT,
    is_weekend BOOLEAN
);

-- Dimension: Weather
CREATE TABLE IF NOT EXISTS dim_weather (
    weather_id        INTEGER PRIMARY KEY,
    date_id           TEXT,
    avg_temp_c        FLOAT,
    precipitation_mm  FLOAT,
    weather_condition TEXT
);

-- Fact: Bike Counts
CREATE TABLE IF NOT EXISTS fact_bike_counts (
    count_id    INTEGER PRIMARY KEY,
    date_id     TEXT,
    station_id  INTEGER,
    weather_id  INTEGER,
    bike_count  INTEGER,
    FOREIGN KEY (date_id)    REFERENCES dim_date(date_id),
    FOREIGN KEY (station_id) REFERENCES dim_station(station_id),
    FOREIGN KEY (weather_id) REFERENCES dim_weather(weather_id)
);
