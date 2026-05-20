# Berlin Analytics Warehouse

Ein lokales Analytics-Data-Warehouse, das Berliner Fahrradzähldaten mit Wetterdaten für das Jahr 2025 kombiniert.  
Entwickelt mit DuckDB, Python und Pandas als Teil des **Berlin Data Engineering Lab** Portfolios.

## Projektübersicht

- **Typ:** Lokales Data Warehouse / SQL Analytics
- **Datenquellen:** Berlin Mobility Pipeline + Berlin Weather Pipeline
- **Warehouse-Engine:** DuckDB
- **Schema:** Sternschema
- **Ziel:** Aufbau eines lokalen Analysemodells, um Fahrradzählungen gemeinsam mit Wetterdaten auszuwerten.

Dieses Projekt verbindet die Ergebnisse aus zwei vorherigen Data-Engineering-Projekten:

1. **Berlin Mobility Pipeline** — bereinigte Fahrradzähldaten
2. **Berlin Weather Pipeline** — bereinigte historische Wetterdaten

Das Ergebnis ist ein lokales DuckDB-Warehouse mit Fakt- und Dimensionstabellen für SQL-Analysen.

## Architektur

1. Einlesen der bereinigten Fahrradzähldaten aus der Berlin Mobility Pipeline.
2. Einlesen der bereinigten Wetterdaten aus der Berlin Weather Pipeline.
3. Laden der Daten in DuckDB.
4. Aufbau eines Sternschemas mit Fakt- und Dimensionstabellen.
5. Ausführen von SQL-Abfragen für analytische Auswertungen.

## Warehouse-Modell

Das Warehouse verwendet ein einfaches Sternschema:

- `fact_bike_counts` — zentrale Faktentabelle mit Fahrradzählungen
- `dim_station` — Informationen zu Zählstationen
- `dim_date` — Datumsdimension für Analysen nach Tag, Monat, Wochentag usw.
- `dim_weather` — Wetterinformationen wie Temperatur, Wind und Niederschlag

## Beispiel-Fragestellungen

Mit diesem Warehouse können unter anderem folgende Fragen analysiert werden:

- Welche Fahrrad-Zählstationen haben die höchsten Werte?
- Wie verändert sich der Fahrradverkehr nach Wochentag?
- Gibt es Unterschiede zwischen Werktagen und Wochenenden?
- Wie hängt die Temperatur mit dem Fahrradverkehr zusammen?
- Gibt es weniger Fahrradverkehr bei Regen oder starkem Wind?
- Welche Monate zeigen die höchste Fahrradaktivität?

## Projektstruktur

```text
berlin-analytics-warehouse/
├── .github/workflows/     # GitHub Actions CI
├── sql/                   # SQL-Abfragen und Warehouse-Logik
├── src/                   # Python-Code zum Einlesen und Erstellen des Warehouses
├── tests/                 # Lokale Tests
├── README.md              # Projektdokumentation
├── requirements.txt       # Python-Abhängigkeiten
└── .gitignore