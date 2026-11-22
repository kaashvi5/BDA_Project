
# Databricks notebook source

# 01 — Bronze Ingestion
# Preserve original columns and attach ingestion metadata.

from pyspark.sql import functions as F

# Catalog and schema configuration
CATALOG = "workspace"
SCHEMA = "tourism_analytics"
TABLE_BASE = f"{CATALOG}.{SCHEMA}"

# Function to write data into Bronze Delta tables
def write_bronze(df, table_name, source_name):

    output = (
        df.withColumn("_ingested_at", F.current_timestamp())
          .withColumn("_source_name", F.lit(source_name))
    )

    (
        output.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(f"{TABLE_BASE}.{table_name}")
    )

    print(f"Saved {table_name}: {output.count()} rows")


# Write all three datasets into Bronze tables

write_bronze(
    visits_raw,
    "bronze_tourism_visits",
    "tourism_visits.csv"
)

write_bronze(
    weather_raw,
    "bronze_weather",
    "weather_daily.csv"
)

write_bronze(
    destinations_raw,
    "bronze_destinations",
    "destinations.csv"
)
