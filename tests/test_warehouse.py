import duckdb
import pytest

DB_PATH = "data/processed/warehouse.duckdb"

@pytest.fixture
def con():
    return duckdb.connect(DB_PATH)

def test_fact_table_not_empty(con):
    count = con.execute("SELECT COUNT(*) FROM fact_bike_counts").fetchone()[0]
    assert count > 0

def test_dim_weather_not_empty(con):
    count = con.execute("SELECT COUNT(*) FROM dim_weather").fetchone()[0]
    assert count > 0

def test_dim_date_not_empty(con):
    count = con.execute("SELECT COUNT(*) FROM dim_date").fetchone()[0]
    assert count > 0
