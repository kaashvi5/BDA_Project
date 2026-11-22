# Project 8 — Tourism: Travel Demand and Destination Intelligence

An end-to-end India-focused data engineering and analytics project using **Databricks Free Edition, PySpark, Delta Lake and Power BI**.

## Objective
Analyze tourist arrivals and destination popularity, seasonal travel trends, domestic vs. foreign visits, destination rankings and the relationship between weather and visitor demand.

## Architecture
Tourism CSV/API data + weather + destination metadata
→ Databricks / PySpark
→ Bronze Delta (raw)
→ Silver Delta (cleaned and standardized)
→ Gold Delta (analytics-ready)
→ Power BI dashboard

## Included
- Databricks notebook source files and an importable `.ipynb`.
- Bronze/Silver/Gold ETL pipeline.
- Schema mapping and validation.
- Synthetic sample CSVs for testing.
- Power BI dashboard design and DAX measures.
- Team responsibility split, project report outline and GitHub README guidance.

> The sample data is synthetic and is only for testing. It must not be presented as actual Indian tourism statistics. Replace it with verified official data for final analysis.

## Databricks setup
1. Open your Databricks Free Edition workspace and start available compute.
2. Create schema `workspace.tourism_analytics` (or change `CATALOG` in notebook 00).
3. Create a Volume named `tourism_raw`.
4. Upload these three CSV files from `sample_data/` to the volume:
   - `tourism_visits.csv`
   - `weather_daily.csv`
   - `destinations.csv`
5. Create a Python notebook and run the notebook cells in order, or import `Tourism_Travel_Demand_Intelligence.ipynb`.
6. Run notebook 00 first and inspect schemas. If you replace the sample files with official datasets, edit `COLUMN_MAP` in notebook 02 to match their actual column names and meanings.

Volume path:
`/Volumes/workspace/tourism_analytics/tourism_raw/`

## Input data contract
### tourism_visits.csv
- `date`: visit date, ISO `yyyy-MM-dd`
- `state`: state/UT
- `destination`: destination name
- `visitor_type`: `Domestic` or `Foreign`
- `visitor_count`: number of visitors for the period

### weather_daily.csv
- `date`: weather observation date
- `state`: matching state/UT name
- `temp_max_c`, `temp_min_c`: temperature in Celsius
- `precipitation_mm`: daily precipitation in millimetres

### destinations.csv
- `destination`, `state`, `latitude`, `longitude`, `category`

The three inputs are intentionally standardized for the starter pipeline. Real datasets may have different levels of aggregation (monthly, yearly, state-level) and definitions. Do not join datasets at mismatched grains. If official tourism data is monthly, aggregate weather to month before joining; do not repeat monthly visitor counts across daily weather rows.

## Run order
| Order | File | Purpose |
|---|---|---|
| 1 | `databricks/00_config_and_inspection.py` | Read files and inspect schemas |
| 2 | `databricks/01_bronze_ingestion.py` | Store raw source data in Bronze Delta |
| 3 | `databricks/02_silver_transform.py` | Clean, standardize and validate |
| 4 | `databricks/03_gold_analytics.py` | Build destination, monthly, visitor-type and weather analytics |
| 5 | `databricks/04_validation_and_export.py` | Validate and export Gold tables for Power BI |

## Official and supplementary data sources
Start with:
- Ministry of Tourism, Government of India: https://tourism.gov.in/
- Open Government Data Platform: https://www.data.gov.in/
- India Tourism Statistics publications: https://tourism.gov.in/market-research-and-statistics
- Open-Meteo historical weather API: https://open-meteo.com/en/docs/historical-weather-api
- OpenStreetMap: https://www.openstreetmap.org/ (destination/location metadata; follow ODbL attribution requirements)

Verify the licence, definitions, coverage period and geographic granularity of each downloaded dataset. Keep a source register with the download date and URL.

## Power BI
Import the exported Gold CSV part files from the Databricks volume. Follow `power_bi/dashboard_guide.md` and copy measures from `power_bi/measures.dax`.

Recommended pages:
1. Tourism Overview
2. Destination Intelligence
3. Seasonal Travel Trends
4. Domestic vs Foreign Visitors
5. Weather and Tourism

## Team split (4 members)
1. **Data sourcing & documentation:** official tourism data, source register, licensing, data dictionary.
2. **Databricks / PySpark:** ingestion, Bronze/Silver/Gold transformations and Delta tables.
3. **Weather & enrichment:** weather data acquisition, destination metadata, location/date matching and validation.
4. **Power BI & QA:** dashboard, DAX, test cases, screenshots and final presentation.
All members should review the integrated pipeline and final numbers.

## Important analytical cautions
- Do not infer causation from correlation between weather and visitor counts.
- Compare only compatible time periods and geographic levels.
- Distinguish tourist visits/arrivals from unique individual tourists if the source does not guarantee uniqueness.
- Keep missing values as null unless the source definition confirms zero.
- Document changes in destination boundaries, state names and reporting methodology.
- Clearly label sample data as synthetic.

## Deliverables
- Source register and data dictionary.
- Bronze, Silver and Gold Delta tables.
- Data quality report.
- Power BI dashboard.
- Architecture diagram and README.
- Final report/presentation with limitations and evidence-based insights.
