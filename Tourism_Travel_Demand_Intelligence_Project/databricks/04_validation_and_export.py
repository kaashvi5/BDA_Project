# Databricks notebook source
# MAGIC %md
# MAGIC # 04 — Validation and Power BI export

from pyspark.sql import functions as F

CATALOG = "workspace"
SCHEMA = "tourism_analytics"
TABLE_BASE = f"{CATALOG}.{SCHEMA}"
EXPORT_BASE = "/Volumes/workspace/tourism_analytics/tourism_raw/powerbi_exports"

gold_tables = [
    "gold_destination_popularity",
    "gold_monthly_trends",
    "gold_visitor_type",
    "gold_weather_tourism",
    "gold_state_overview"
]

for table_name in gold_tables:
    df = spark.table(f"{TABLE_BASE}.{table_name}")
    count = df.count()
    print(f"{table_name}: {count} rows")
    if count == 0:
        raise ValueError(f"{table_name} is empty")
    display(df.limit(5))

# Export as CSV folders. Download the part-*.csv file within each folder.
for table_name in gold_tables:
    (spark.table(f"{TABLE_BASE}.{table_name}")
        .coalesce(1)
        .write.mode("overwrite")
        .option("header", True)
        .csv(f"{EXPORT_BASE}/{table_name}"))

print("All Gold tables validated and exported.")
