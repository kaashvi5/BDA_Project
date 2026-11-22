# Databricks notebook source
# MAGIC %md
# MAGIC # 00 — Configuration and source inspection
# MAGIC Run this first. Upload CSVs to the configured Unity Catalog Volume.

from pyspark.sql import functions as F

CATALOG = "workspace"
SCHEMA = "tourism_analytics"
VOLUME = "tourism_raw"
BASE_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"
TABLE_BASE = f"{CATALOG}.{SCHEMA}"

VISITS_PATH = f"{BASE_PATH}/tourism_visits.csv"
WEATHER_PATH = f"{BASE_PATH}/weather_daily.csv"
DESTINATIONS_PATH = f"{BASE_PATH}/destinations.csv"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

def read_csv(path):
    return (spark.read.option("header", True)
            .option("inferSchema", True)
            .option("mode", "PERMISSIVE")
            .csv(path))

visits_raw = read_csv(VISITS_PATH)
weather_raw = read_csv(WEATHER_PATH)
destinations_raw = read_csv(DESTINATIONS_PATH)

for name, df in [
    ("TOURISM VISITS", visits_raw),
    ("WEATHER", weather_raw),
    ("DESTINATIONS", destinations_raw)
]:
    print(f"\n{name}")
    df.printSchema()
    print("Rows:", df.count())
    display(df.limit(10))
