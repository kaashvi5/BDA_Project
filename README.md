# 🌍 TourismPulse — Travel Demand Intelligence

**An End-to-End Tourism Analytics & Business Intelligence Project**

Transforming tourism, destination, and weather data into meaningful insights using **Databricks, PySpark, Delta Lake, SQL, and Power BI.**

---

## 📌 Project Overview

TourismPulse is a data engineering and business intelligence project designed to analyze tourism trends, understand destination popularity, identify seasonal travel patterns, and explore the relationship between weather conditions and tourism demand.

The project follows a modern **Medallion Architecture (Bronze → Silver → Gold)** to process raw datasets, clean and transform information, generate analytical tables, and prepare data for interactive Power BI dashboards.

The ultimate goal is to convert raw tourism data into actionable insights that can support tourism planning and data-driven decision-making.

## 🎯 Project Objectives

- Analyze tourism demand across different states and destinations.
- Identify popular tourist destinations based on visitor counts.
- Understand monthly and seasonal tourism trends.
- Compare domestic and foreign visitor patterns.
- Explore relationships between weather conditions and tourism activity.
- Build a structured and scalable data processing pipeline.
- Develop interactive business intelligence dashboards.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and pipeline development |
| PySpark | Large-scale data transformation |
| Databricks | Cloud-based data engineering |
| Delta Lake | Structured data storage |
| SQL | Data querying and management |
| Unity Catalog | Data organization and governance |
| Power BI | Interactive dashboards and visualization |
| DAX | Dashboard calculations and KPIs |
| Git & GitHub | Version control and project management |

## 🏗️ Project Architecture

The project follows the Medallion Architecture.

```text
              SOURCE DATA
                    |
        +-----------+-----------+
        |           |           |
     Tourism     Weather    Destinations
        |           |           |
        +-----------+-----------+
                    |
                    v
             DATABRICKS
                    |
                    v
             BRONZE LAYER
          Raw Ingested Data
                    |
                    v
             SILVER LAYER
       Cleaning and Transformation
                    |
                    v
              GOLD LAYER
          Business Aggregations
                    |
                    v
                POWER BI
                    |
                    v
        Interactive Dashboards
```

### 1. Bronze Layer — Raw Data Ingestion

- Ingests the original tourism, weather, and destination datasets.
- Preserves source columns.
- Adds ingestion timestamps and source metadata.
- Stores the datasets as Delta tables.

### 2. Silver Layer — Data Transformation

- Cleans and standardizes the datasets.
- Converts dates and numerical fields into appropriate data types.
- Removes duplicate records.
- Handles invalid and missing values.
- Enriches tourism data using destination and weather information.

### 3. Gold Layer — Business Analytics

Creates five analytics-ready tables:

| Gold Table | Purpose |
|---|---|
| gold_destination_popularity | Destination-wise visitor analysis |
| gold_monthly_trends | Monthly tourism trends |
| gold_visitor_type | Domestic vs foreign visitor analysis |
| gold_weather_tourism | Weather and tourism comparison |
| gold_state_overview | State-level tourism overview |

These tables are designed for reporting and dashboard development.

## 📂 Project Structure

```text
Tourism_Travel_Demand_Intelligence_Project/
│
├── README.md
│
├── Tourism_Travel_Demand_Intelligence.ipynb
│
├── sample_data/
│   ├── tourism_visits.csv
│   ├── weather_daily.csv
│   └── destinations.csv
│
├── databricks/
│   ├── 00_config_and_inspection.py
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_transform.py
│   ├── 03_gold_analytics.py
│   └── 04_validation_and_export.py
│
├── data/
│   ├── gold_destination_popularity.csv
│   ├── gold_monthly_trends.csv
│   ├── gold_state_overview.csv
│   ├── gold_visitor_type.csv
│   └── gold_weather_tourism.csv
│
├── power_bi/
│   ├── dashboard_guide.md
│   └── measures.dax
│
├── dashboard/
│   ├── index.html
│   └── vercel.json
│
└── docs/
    └── project_report_outline.md
```

## 📊 Dataset Description

The project currently includes three input datasets.

| Dataset | Description |
|---|---|
| tourism_visits.csv | Tourism visitor counts, dates, destinations and visitor types |
| weather_daily.csv | Daily maximum/minimum temperatures and precipitation |
| destinations.csv | Destination names, states, coordinates and categories |

**Important:** The included sample datasets are synthetic testing data. They are intended to demonstrate and validate the pipeline, not to represent actual Indian tourism statistics.

For real-world analysis, replace them with verified official datasets and document their sources, definitions, licensing, and coverage.

## ⚙️ Installation & Execution

### Step 1 — Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Tourism_Travel_Demand_Intelligence_Project
```

### Step 2 — Open Databricks

1. Log in to your Databricks workspace.
2. Start the available compute.
3. Check your Unity Catalog permissions.
4. Select an accessible catalog and schema.

### Step 3 — Configure Data Storage

The starter scripts currently use:

```python
CATALOG = "workspace"
SCHEMA = "tourism_analytics"
VOLUME = "tourism_raw"
```

Create the required schema and volume if you have the necessary privileges. If your workspace does not grant CREATE SCHEMA on `workspace`, use an administrator-approved schema or catalog and update the configuration consistently across the notebooks.

### Step 4 — Upload Input Datasets

Upload these three files to the configured Unity Catalog Volume:

- tourism_visits.csv
- weather_daily.csv
- destinations.csv

### Step 5 — Execute the Pipeline

Run the notebooks in the following order:

| Order | Notebook | Operation |
|---|---|---|
| 01 | 00_config_and_inspection.py | Configuration and data inspection |
| 02 | 01_bronze_ingestion.py | Bronze ingestion |
| 03 | 02_silver_transform.py | Data cleaning and transformation |
| 04 | 03_gold_analytics.py | Gold analytics generation |
| 05 | 04_validation_and_export.py | Validation and CSV exports |

Alternatively, import the provided `.ipynb` notebook into Databricks.

### Step 6 — Power BI Integration

1. Execute the Gold layer successfully.
2. Run the validation and export notebook.
3. Download the exported CSV part files.
4. Import the five Gold datasets into Power BI.
5. Configure relationships, measures, slicers, and visualizations.
6. Build the interactive dashboards.

Refer to `power_bi/dashboard_guide.md` for dashboard specifications and `power_bi/measures.dax` for measures.

## 📈 Planned Dashboard Pages

The Power BI dashboard design includes five analytical pages:

1. **Tourism Overview** — Overall visitor KPIs and state-level tourism trends.
2. **Destination Intelligence** — Popular destinations and destination rankings.
3. **Seasonal Travel Trends** — Monthly and quarterly tourism patterns.
4. **Domestic vs Foreign Visitors** — Visitor segmentation and comparisons.
5. **Weather & Tourism** — Temperature, precipitation, and tourism comparisons.

## 📁 Expected Deliverables

- Structured Bronze, Silver, and Gold Delta tables.
- Five Gold analytical datasets.
- Data quality and validation results.
- Interactive Power BI dashboards.
- Project documentation and architecture.
- Final project report and presentation.

## ⚠️ Important Considerations

- Verify dataset definitions and reporting periods before combining sources.
- Match the geographical and temporal granularity of tourism and weather datasets.
- Do not interpret correlation as proof of causation.
- Preserve missing values unless the source confirms that they represent zero.
- Clearly identify synthetic datasets in testing and demonstration outputs.

## 🚀 Future Enhancements

- Integrate verified Ministry of Tourism datasets.
- Automate scheduled data ingestion and refresh.
- Add tourism demand forecasting using machine learning.
- Develop destination recommendation capabilities.
- Introduce real-time tourism trend monitoring.
- Deploy interactive dashboards for wider accessibility.

## 👩‍💻 Project Information

**Project Name:** TourismPulse — Travel Demand Intelligence  
**Domain:** Data Engineering, Tourism Analytics & Business Intelligence  
**Architecture:** Medallion Architecture  
**Primary Tools:** Databricks, PySpark, Delta Lake, SQL and Power BI

---

**TourismPulse — Turning Travel Data Into Intelligent Decisions.** 🌍
