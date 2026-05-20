# Berlin Analytics Warehouse

Ein lokales Analytics-Data-Warehouse, das Berliner Fahrradzähldaten mit Wetterdaten (2025) kombiniert.
Entwickelt mit DuckDB, Python und Pandas als Teil des Berlin Data Engineering Lab Portfolios.

## Projektübersicht

- **Typ:** Lokales Data Warehouse / SQL Analytics
- **Datenquellen:** Berlin Mobility Pipeline + Berlin Weather Pipeline
- **Warehouse-Engine:** DuckDB
- **Schema:** Sternschema (1 Faktentabelle + 3 Dimensionstabellen)

## Architektur
Rohdaten (Parquet)
↓
src/ingest.py
↓
DuckDB Warehouse
├── fact_bike_counts
├── dim_station
├── dim_date
└── dim_weather
↓
sql/analysis.sql → notebooks/analysis.ipynb → Diagramme


## Wichtige Erkenntnisse

- An Regentagen gibt es ca. 15 % weniger Fahrradfahrten als an trockenen Tagen
- Die Hauptverkehrszeiten sind 8 Uhr morgens und 17–18 Uhr abends
- Werktage haben 62 % mehr Fahrradverkehr als Wochenenden
- Juni ist der verkehrsreichste Monat mit über 3 Millionen Zählungen

## Technologien

`Python` `DuckDB` `Pandas` `Matplotlib` `Seaborn` `Jupyter`

## Ausführung

```bash
pip install -r requirements.txt
python3 src/ingest.py
jupyter notebook notebooks/analysis.ipynb
``
